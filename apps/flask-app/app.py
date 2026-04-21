from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
