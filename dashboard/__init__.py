from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or 'sqlite:///database.db'
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config['GITHUB_REDIRECT_URL'] = os.environ.get("GITHUB_REDIRECT_URL")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
app.config["GITHUB_LAB_USER"] = os.environ.get("GITHUB_LAB_USER")
app.config["GOOGLE_GLOBAL_SITE_TAG"] = os.environ.get("GOOGLE_GLOBAL_SITE_TAG")

admins = os.environ.get("DASHBOARD_ADMIN") or ""
app.config["DASHBOARD_ADMIN"] = []
for admin in admins.split(","):
    app.config["DASHBOARD_ADMIN"].append(admin.strip())

from dashboard import routes, models



