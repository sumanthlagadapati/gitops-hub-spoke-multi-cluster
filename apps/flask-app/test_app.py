import os
import socket
import pytest
from flask import Flask
from app import app, traffic_metrics

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset metrics before each test
        with traffic_metrics['lock']:
            traffic_metrics['total_requests'] = 0
            traffic_metrics['per_route'] = {}
        yield client

def login(client, username, password):
    # Users are now in the database
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

def register(client, username, password, role='viewer'):
    return client.post('/register', data={'username': username, 'password': password, 'role': role}, follow_redirects=True)

def logout(client):
    return client.post('/logout', follow_redirects=True)

def request_password_reset(client, username):
    return client.post('/reset_password_request', data={'username': username}, follow_redirects=True)

def reset_password(client, token, new_password):
    return client.post(f'/reset_password/{token}', data={'password': new_password}, follow_redirects=True)

def test_dashboard_metrics_increment(client):
    # Login as viewer
    login(client, 'viewer', 'viewerpass')
    # Initial dashboard state
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert b'Total Requests:' in rv.data
    assert b'/dashboard' in rv.data or b'dashboard' in rv.data
    # Hit root and health endpoints
    client.get('/')
    client.get('/health')
    # Dashboard should now show increased counts
    rv2 = client.get('/dashboard')
    assert b'Total Requests:' in rv2.data
    assert b'/dashboard' in rv2.data or b'dashboard' in rv2.data
    assert b'/health' in rv2.data or b'health' in rv2.data
    assert b'hello' in rv2.data or b'/' in rv2.data
    # Check that total_requests increased
    # Parse the HTML to extract the total_requests value
    import re
    match = re.search(br'Total Requests:</b>\s*(\d+)', rv2.data)
    assert match, "Total Requests not found in dashboard HTML"
    total_requests = int(match.group(1))
    assert total_requests >= 4  # dashboard, /, /health, dashboard again
    logout(client)

def test_dashboard_cluster_info(client):
    # Login as viewer
    login(client, 'viewer', 'viewerpass')
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert os.getenv('CLUSTER_NAME', 'unknown').encode() in rv.data
    assert os.getenv('ENVIRONMENT', 'dev').encode() in rv.data
    assert socket.gethostname().encode() in rv.data
    assert b'v1.0.0' in rv.data
    logout(client)

    # Test forbidden for not logged in
    rv2 = client.get('/dashboard')
    assert rv2.status_code == 302 or rv2.status_code == 401 or rv2.status_code == 403

def test_api_clusters(client):
    # Login as admin
    login(client, 'admin', 'adminpass')
    rv = client.get('/api/clusters')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Check that required keys exist in at least one cluster
    cluster = data[0]
    assert 'name' in cluster
    assert 'environment' in cluster
    assert 'status' in cluster
    logout(client)

    # Test forbidden for viewer
    login(client, 'viewer', 'viewerpass')

def test_password_reset_flow(client):
    # Register a new user
    username = 'resetuser'
    password = 'oldpass'
    new_password = 'newpass123'
    register(client, username, password)
    logout(client)
    # Request password reset
    rv = request_password_reset(client, username)
    assert b'Password reset link' in rv.data
    import re
    m = re.search(br'/reset_password/([\w\-_=]+)', rv.data)
    assert m, 'Reset link not found in response'
    token = m.group(1).decode()
    # Use the reset link to set a new password
    rv2 = reset_password(client, token, new_password)
    assert b'Password reset successful' in rv2.data
    # Login with new password
    rv3 = login(client, username, new_password)
    assert b'Dashboard' in rv3.data or b'dashboard' in rv3.data
    logout(client)
   rv2 = client.get('/api/clusters')
    assert rv2.status_code == 403
    data2 = rv2.get_json()
    assert data2['error'].startswith('Forbidden')
    logout(client)

def test_api_clusters_auth_required(client):
    rv = client.get('/api/clusters')
    assert rv.status_code == 401
    data = rv.get_json()
    assert data['error'] == 'Unauthorized'

def test_registration_and_audit_log(client):
    # Register a new user
    username = 'testuser'
    password = 'testpass123'
    register(client, username, password, 'viewer')
    # Login as new user
    login(client, username, password)
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    # Logout
    logout(client)
    # Login as admin and check audit log
    login(client, 'admin', 'adminpass')
    rv = client.get('/admin/audit_log')
    assert rv.status_code == 200
    assert b'testuser' in rv.data
    assert b'register' in rv.data
    assert b'login' in rv.data
    logout(client)
