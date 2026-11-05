"""Фабрика створення Flask-додатка."""

from flask import Flask
from .config import config_by_name
from .views import register_routes


def create_app(config_name: str = 'development') -> Flask:
    """Фабрика додатка Flask."""
    app = Flask(__name__)

    # Завантажуємо конфігурацію
    app.config.from_object(config_by_name[config_name])

    # Реєструємо маршрути
    register_routes(app)

    return app