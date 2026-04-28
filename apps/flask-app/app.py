from flask import Flask, jsonify, render_template_string, request
import os
import socket
import threading

app = Flask(__name__)

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
    cluster = os.getenv("CLUSTER_NAME", "unknown")
    environment = os.getenv("ENVIRONMENT", "dev")
    hostname = socket.gethostname()
    version = "v1.0.0"
    with traffic_metrics['lock']:
        total_requests = traffic_metrics['total_requests']
        per_route = dict(traffic_metrics['per_route'])
    html = '''
    <html>
    <head><title>Cluster Status Dashboard</title></head>
    <body>
        <h1>Cluster Status Dashboard</h1>
        <ul>
            <li><b>Cluster:</b> {{ cluster }}</li>
            <li><b>Environment:</b> {{ environment }}</li>
            <li><b>Hostname:</b> {{ hostname }}</li>
            <li><b>Version:</b> {{ version }}</li>
        </ul>
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
        per_route=per_route
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
