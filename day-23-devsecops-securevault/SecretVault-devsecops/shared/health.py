from flask import jsonify


def health_response(service_name: str, version: str = "1.0.0"):
    return jsonify({"status": "healthy", "service": service_name, "version": version})
