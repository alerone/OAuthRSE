from flask import Flask, render_template, url_for, redirect, session
import hashlib
import os
import json
from pathlib import Path
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

secrets = json.loads(Path("secrets.json").read_text())["installed"]

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",  
    "https://www.googleapis.com/auth/userinfo.profile"   
]

app.secret_key = hashlib.sha256(os.urandom(1024)).hexdigest()

oauth = OAuth(app)

oauth.register(
    "google",
    client_id = secrets["client_id"],
    client_secret = secrets["client_secret"],
    access_token_url = secrets["token_uri"],
    authorize_url = secrets["auth_uri"],
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    client_kwargs = {
        "scope": " ".join(SCOPES)    
    },
)

@app.route("/")
def home():
    user = session.get("user")
    if user:
        return render_template('welcome.html', user = user)
    return (render_template("home.html"))

@app.route("/login")
def login():
    redirect_uri = url_for('authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri, prompt = 'select_account')


@app.route("/auth/callback")
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get('userinfo').json()
    session['user'] = {
        'name': user_info.get('name'),
        'email': user_info.get('email'),
        'picture': user_info.get('picture') 
    }
    print(user_info)
    return redirect('/')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)