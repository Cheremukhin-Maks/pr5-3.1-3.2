"""Конфігурація Flask-додатка."""

import os


class Config:
    """Базова конфігурація."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-12345')
    DEBUG = False


class DevelopmentConfig(Config):
    """Конфігурація для розробки."""
    DEBUG = True


class ProductionConfig(Config):
    """Конфігурація для production."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
