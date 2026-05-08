from flask import Flask, jsonify, render_template_string, request, session, redirect, url_for
import os
import socket
import threading

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# USERS dict is now deprecated; users are stored in the database
# USERS = {
#     'admin': {'password': 'adminpass', 'role': 'admin'},
#     'viewer': {'password': 'viewerpass', 'role': 'viewer'}
# }

# In-memory traffic metrics
traffic_metrics = {
    'total_requests': 0,
    'per_route': {},
    'lock': threading.Lock()
}

@app.before_request
def count_requests():
    route = request.endpoint or request.path
    with traffic_metrics['lock']:
        traffic_metrics['total_requests'] += 1
        if route not in traffic_metrics['per_route']:
            traffic_metrics['per_route'][route] = 0
        traffic_metrics['per_route'][route] += 1

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from GitOps Hub & Spoke!",
        "cluster": os.getenv("CLUSTER_NAME", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "hostname": socket.gethostname(),
        "version": "v1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_role = session.get('role', 'viewer')
    if user_role not in ['admin', 'viewer']:
        return "<h2>Forbidden: viewer or admin role required</h2>", 403
    cluster = os.getenv("CLUSTER_NAME", "unknown")
    environment = os.getenv("ENVIRONMENT", "dev")
    hostname = socket.gethostname()
    version = "v1.0.0"
    with traffic_metrics['lock']:
        total_requests = traffic_metrics['total_requests']
        per_route = dict(traffic_metrics['per_route'])
    html = '''
    <html>
    <head>
        <title>Cluster Status Dashboard</title>
        <script>
        function loadClusters() {
            fetch('/api/clusters')
                .then(response => response.json())
                .then(data => {
                    const table = document.getElementById('clusters-table-body');
                    table.innerHTML = '';
                    if (data.error) {
                        table.innerHTML = `<tr><td colspan='3' style='color:red;'>${data.error}</td></tr>`;
                        return;
                    }
                    data.forEach(c => {
                        let color = c.status === 'Healthy' ? 'green' : (c.status === 'Degraded' ? 'orange' : 'red');
                        let icon = c.status === 'Healthy' ? '●' : (c.status === 'Degraded' ? '●' : '●');
                        table.innerHTML += `<tr><td>${c.name}</td><td>${c.environment}</td><td style='color:${color};font-weight:bold;'>${icon} ${c.status}</td></tr>`;
                    });
                })
                .catch(err => {
                    const table = document.getElementById('clusters-table-body');
                    table.innerHTML = `<tr><td colspan='3' style='color:red;'>Failed to load clusters</td></tr>`;
                });
        }
        document.addEventListener('DOMContentLoaded', function() {
            loadClusters();
            setInterval(loadClusters, 10000);
        });
        </script>
    </head>
    <body>
        <h1>Cluster Status Dashboard</h1>
        <div style="float:right;"><form method="post" action="/logout"><button type="submit">Logout ({{ session['username'] }})</button></form></div>
        <ul>
            <li><b>Cluster:</b> {{ cluster }}</li>
            <li><b>Environment:</b> {{ environment }}</li>
            <li><b>Hostname:</b> {{ hostname }}</li>
            <li><b>Version:</b> {{ version }}</li>
            <li><b>Role:</b> {{ session['role'] }}</li>
        </ul>
        <h2>Multi-Cluster Deployment Visualizer</h2>
        <div style="margin-bottom:10px;">
            <b>Legend:</b>
            <span style="color:green;font-weight:bold;">● Healthy</span>
            <span style="color:orange;font-weight:bold;">● Degraded</span>
            <span style="color:red;font-weight:bold;">● Unreachable</span>
        </div>
        <table border="1" style="margin-bottom:20px;">
            <tr><th>Cluster Name</th><th>Environment</th><th>Status</th></tr>
            <tbody id="clusters-table-body">
                <tr><td colspan="3">Loading...</td></tr>
            </tbody>
        </table>
        <h2>Traffic Metrics</h2>
        <ul>
            <li><b>Total Requests:</b> {{ total_requests }}</li>
        </ul>
        <h3>Requests per Route</h3>
        <table border="1">
            <tr><th>Route</th><th>Count</th></tr>
            {% for route, count in per_route.items() %}
            <tr><td>{{ route }}</td><td>{{ count }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html,
        cluster=cluster,
        environment=environment,
        hostname=hostname,
        version=version,
        total_requests=total_requests,
        per_route=per_route,
        session=session
    )

import sqlite3

def get_clusters_from_db():
    db_path = os.path.join(os.path.dirname(__file__), 'clusters.db')
    clusters = []
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        for row in c.execute('SELECT name, environment, status FROM clusters'):
            clusters.append({
                'name': row[0],
                'environment': row[1],
                'status': row[2]
            })
        conn.close()
    except Exception as e:
        return None, str(e)
    return clusters, None

@app.route('/api/clusters')
def api_clusters():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if session.get('role') != 'admin':
        return jsonify({'error': 'Forbidden: admin role required'}), 403
    clusters, err = get_clusters_from_db()
    if err:
        return jsonify({'error': 'Failed to load clusters', 'details': err}), 500
    return jsonify(clusters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Authenticate against users table in DB
        db_path = os.path.join(os.path.dirname(__file__), 'clusters.db')
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('SELECT password, role FROM users WHERE username = ?', (username,))
            row = c.fetchone()
            conn.close()
            if row and row[0] == password:
                session['username'] = username
                session['role'] = row[1]
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password'
        except Exception as e:
            error = f'Login error: {e}'
    html = '''
    <html><head><title>Login</title></head><body>
    <h2>Login</h2>
    {% if error %}<p style=\"color:red;\">{{ error }}</p>{% endif %}
    <form method=\"post\">
        <label>Username: <input name=\"username\"></label><br>
        <label>Password: <input name=\"password\" type=\"password\"></label><br>
        <button type=\"submit\">Login</button>
    </form>
    </body></html>
    '''
    return render_template_string(html, error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
