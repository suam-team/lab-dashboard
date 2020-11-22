from flask import Flask, request, render_template, redirect, session
from flask_dance.contrib.github import make_github_blueprint, github
from github import Github, GithubException

import json
import base64
import bcrypt

from . models import User, Lab, db, Solve
from . util import decrypt_flag, encrypt_flag

from dashboard import app

github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")

github_sdk = Github()

def fetch_user(func):
    def wrapper_fetch_user(*args, **kwargs):
        if github.authorized:
            if not session.get("user_id"):
                r = github.get("/user")
                github_user = json.loads(r.text)
                user = User.query.filter(User.id==github_user["id"]).first()

                if user:
                    user.github_login = github_user["login"]
                else:
                    user = User(github_user["id"], github_user["login"], github_user["login"], "")
                    db.session.add(user)
                    
                db.session.commit()
                db.session.refresh(user)
                session["user_id"] = user.id
                
            else:
                user = User.query.filter(User.id==session["user_id"]).first()
            
            session["user"] = user.to_dict()
            session["user"]["is_admin"] = session["user"]["github_login"] in app.config["DASHBOARD_ADMIN"]
            db.session.close()

        return func(*args, **kwargs)

    wrapper_fetch_user.__name__ = func.__name__
    return wrapper_fetch_user

def authen(func):
    def wrapper_authen(*args, **kwargs):
        if not github.authorized:
            return redirect("/")

        return func(*args, **kwargs)

    wrapper_authen.__name__ = func.__name__
    return wrapper_authen

@app.route('/')
@fetch_user
def index():
    current_user = session.get("user")
    msg = request.args.get("msg")
    labs = Lab.query.all()
    resp = render_template('index.html', msg=msg, current_user=current_user, labs=labs)
    db.session.close()
    return resp

@app.route('/sync')
@authen
@fetch_user
def sync():
    current_user = session.get("user")
    if not current_user["is_admin"]:
        return redirect("/")

    github_user = github_sdk.get_user(app.config["GITHUB_LAB_USER"])

    existing_labs = []

    for repo in github_user.get_repos():
        repo_name = repo.full_name
        url = f"https://github.com/{repo_name}"
        
        try:
            lab_file = repo.get_contents("lab.json")
        except GithubException:
            continue
        
        lab = json.loads(base64.b64decode(lab_file.content))

        if "name" not in lab or "category" not in lab or "flag" not in lab or "detail" not in lab:
            continue

        existing_labs.append(repo_name)

        existing_lab = Lab.query.filter(Lab.repo_name==repo_name).first()

        if existing_lab:
            existing_lab.name = lab["name"]
            existing_lab.url = url
            existing_lab.category = lab["category"]
            existing_lab.flag = decrypt_flag(lab["flag"], app.secret_key)
            existing_lab.detail = lab["detail"]
        else:
            lab = Lab(repo_name, lab["name"], lab["category"], url, decrypt_flag(lab["flag"], app.secret_key), lab["detail"])
            db.session.add(lab)
    
    deleted_labs = Lab.query.filter(Lab.repo_name.notin_(existing_labs)).all()
    
    for deleted_lab in deleted_labs:
        db.session.delete(deleted_lab)

    db.session.commit()
    db.session.close()

    return redirect("/?msg=Sync+Complete")

@app.route('/enc_flag')
@authen
@fetch_user
def enc_flag():
    current_user = session.get("user")
    if not current_user["is_admin"]:
        return redirect("/")

    if not request.args.get("flag"):
        return redirect("/")

    return encrypt_flag(request.args.get("flag"), app.secret_key)

@app.route('/lab/<path:repo_name>')
@fetch_user
def lab(repo_name):
    current_user = session.get("user")
    msg = request.args.get("msg")
    lab = Lab.query.filter(Lab.repo_name==repo_name).first()
    solve = None
    if current_user:
        solve = Solve.query.filter(Solve.lab_repo_name==repo_name, Solve.user_id==current_user["id"]).first()
    resp = render_template('lab.html', msg=msg, current_user=current_user, lab=lab, is_solve=(solve != None), is_auth=(current_user != None))
    db.session.close()
    return resp

@app.route('/lab/solve', methods=["POST"])
@authen
@fetch_user
def solve():
    current_user = session.get("user")
    flag = request.form.get("flag")
    repo_name = request.form.get("repo_name")

    existing_solve = Solve.query.filter(Solve.user_id==current_user["id"], Solve.lab_repo_name==repo_name).first()

    if existing_solve:
        return redirect(f"/lab/{repo_name}?msg=You+have+already+solved+this+lab.")
    
    lab = Lab.query.filter(Lab.repo_name == repo_name).first()

    if not lab:
        return redirect('/')

    if bcrypt.checkpw(flag.encode(), lab.flag.encode()):
        solve = Solve(current_user["id"], lab.repo_name)
        db.session.add(solve)
        db.session.commit()
        db.session.close()
        return redirect(f"/lab/{repo_name}?msg=Congratulation!")
    else:
        return redirect(f"/lab/{repo_name}?msg=Invalid+Flag")


@app.route('/profile', methods=["GET", "POST"])
@authen
@fetch_user
def profile():
    if request.method == 'POST':

        nickname = request.form.get("nickname")
        comment = request.form.get("comment")

        current_user = User.query.filter(User.id==session["user"]["id"]).first()
        if nickname:
            current_user.nickname = nickname
        if comment:
            current_user.comment = comment
        
        db.session.commit()
        db.session.refresh(current_user)
        db.session.close()

        return redirect("/profile?msg=Update+Profile+Success")
    else:
        msg = request.args.get("msg")
        current_user = session.get("user")

        return render_template('profile.html', msg=msg, current_user=current_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')