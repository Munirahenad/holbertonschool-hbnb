# part2/app.py
from flask import Flask
from api.v1 import api_v1_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_v1_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
