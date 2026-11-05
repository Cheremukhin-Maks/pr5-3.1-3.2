"""Маршрути додатка Flask."""

import flask
from flask import Flask, jsonify, request


def register_routes(app: Flask):
    """Реєструє маршрути додатка."""

    @app.route('/')
    def index():
        """Головна сторінка."""
        return """
        <h1>Ласкаво просимо до Flask-додатка!</h1>
        <p>Корисні посилання:</p>
        <ul>
            <li><a href="/about">Про додаток (/about)</a></li>
            <li><a href="/api/info">API Info (/api/info)</a></li>
            <li><a href="/greet">Привітання (/greet)</a></li>
            <li><a href="/greet/Олексій">Динамічне привітання (/greet/Олексій)</a></li>
        </ul>
        """

    @app.route('/about')
    def about():
        """Сторінка 'Про додаток'."""
        return """
        <h1>Про проект</h1>
        <p>Це Flask-додаток, створений у рамках Практичної роботи №5.</p>
        <p>Використовує патерн <b>Application Factory</b>.</p>
        <a href="/">← На головну</a>
        """

    @app.route('/api/info')
    def api_info():
        """API-ендпоінт з інформацією у JSON."""
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        return jsonify({
            'framework': 'Flask',
            'version': flask.__version__,
            'debug': app.config['DEBUG'],
            'routes': routes
        })

    @app.route('/greet')
    @app.route('/greet/<name>')
    def greet(name=None):
        """Маршрут з динамічним параметром та query-параметром."""
        if not name:
            name = request.args.get('name', 'Гість')
            
        return f"""
        <h1>Привіт, {name}!</h1>
        <p>Раді тебе бачити на нашому сервері.</p>
        <a href="/">← На головну</a>
        """
