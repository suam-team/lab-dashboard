# Lab Dashboard

The hacking lab dashboard that lists labs from the Github user. For our lab dashboard, please navigate to [https://suam-lab-dashboard.herokuapp.com/](https://suam-lab-dashboard.herokuapp.com/).

## Avaliable Features

- Authentication with Github OAuth
- Sync labs from Github user
- Submit flag

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

Please note that the Github application is required (https://github.com/settings/developers). Set `Authorization callback URL` to https://[YOUR_DASHBOARD]/login/github/authorized.

```sh
$ git clone https://github.com/suam-team/lab-dashboard.git
$ cd lab-dashboard
$ pip install -r requirements.txt
$ cp .env.example .env
# Edit environment variables
$ vi .env 
# DATABASE_URL: Database connection string
# GITHUB_OAUTH_CLIENT_ID: Github app OAuth client ID
# GITHUB_OAUTH_CLIENT_SECRET: Github app OAuth secret
# DASHBOARD_ADMIN: Github ID for dashboard admin (for encrypting flag and syncing lab)
# GITHUB_LAB_USER: Target Github user to sync labs
# SECRET_KEY: Dashboard secret key
# GOOGLE_GLOBAL_SITE_TAG: Global Site TAG for google analytic
# PREFERRED_URL_SCHEME: Set URL Schema for app behide reverse proxy
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku main
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Contibuting

Please navigate to [CONTRIBUTING.md](/CONTRIBUTING.md).