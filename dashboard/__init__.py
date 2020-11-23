from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or 'sqlite:///database.db'
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
app.config["GITHUB_LAB_USER"] = os.environ.get("GITHUB_LAB_USER")
app.config["GOOGLE_GLOBAL_SITE_TAG"] = os.environ.get("GOOGLE_GLOBAL_SITE_TAG")
app.config['PREFERRED_URL_SCHEME'] = os.environ.get("PREFERRED_URL_SCHEME")

admins = os.environ.get("DASHBOARD_ADMIN") or ""
app.config["DASHBOARD_ADMIN"] = []
for admin in admins.split(","):
    app.config["DASHBOARD_ADMIN"].append(admin.strip())

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = app.config['PREFERRED_URL_SCHEME']
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

app.wsgi_app = ReverseProxied(app.wsgi_app)

from dashboard import routes, models



