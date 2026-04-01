from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "name": "claw-code",
        "description": "Python porting workspace for the Claw Code rewrite effort",
        "endpoints": ["/summary", "/manifest", "/subsystems", "/health"],
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/summary")
def summary():
    from src.port_manifest import build_port_manifest
    manifest = build_port_manifest()
    return jsonify(manifest.__dict__ if hasattr(manifest, "__dict__") else str(manifest))


@app.route("/manifest")
def manifest():
    from src.port_manifest import build_port_manifest
    manifest = build_port_manifest()
    return jsonify(manifest.__dict__ if hasattr(manifest, "__dict__") else str(manifest))


@app.route("/subsystems")
def subsystems():
    import importlib, pkgutil, src
    modules = [m.name for m in pkgutil.iter_modules(src.__path__)]
    return jsonify({"subsystems": modules, "count": len(modules)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
