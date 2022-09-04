from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY'),
        MY_EMAIL=os.environ.get('MY_EMAIL')
    )

    from . import portfolio

    app.register_blueprint(portfolio.bp)

    return app
