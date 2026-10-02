"""A small web UI for every project in this repo.

Run it from the repo root with:  python -m arcade
"""
import os
import secrets

from flask import Flask

# No inline script or style anywhere, so the policy can stay strict.
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'")


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        # Sessions only hold game state, so a fresh key per run is fine;
        # set SECRET_KEY to keep sessions across restarts.
        SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        SESSION_COOKIE_SAMESITE='Lax',    # no cross-site form posts with our cookie
    )
    if config:
        app.config.update(config)

    from .views import bp
    app.register_blueprint(bp)

    @app.after_request
    def security_headers(response):
        response.headers.setdefault('Content-Security-Policy', CSP)
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('Referrer-Policy', 'same-origin')
        return response

    return app
