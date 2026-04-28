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

def test_dashboard_metrics_increment(client):
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

def test_dashboard_cluster_info(client):
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert os.getenv('CLUSTER_NAME', 'unknown').encode() in rv.data
    assert os.getenv('ENVIRONMENT', 'dev').encode() in rv.data
    assert socket.gethostname().encode() in rv.data
    assert b'v1.0.0' in rv.data
