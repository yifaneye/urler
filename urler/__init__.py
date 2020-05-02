from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)  # app
    app.secret_key = 'r9qy-T2c1-ieO8-a951-dBVj-kAo8'
    from . import urler
    app.register_blueprint(urler.bp)
    return app
