from flask import Blueprint, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import json
from pathlib import Path
from db.user_crud import create_user, get_user_by_email

secrets_path = Path(__file__).resolve().parent / "secrets.json"
secrets = json.loads(secrets_path.read_text())["installed"]

auth_bp = Blueprint('auth', __name__)

oauth = OAuth()

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",  
    "https://www.googleapis.com/auth/userinfo.profile"   
]

google = oauth.register(
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

@auth_bp.route("/login")
def login():
    redirect_uri = url_for('auth.authorize', _external = True)
    return google.authorize_redirect(redirect_uri, prompt = 'select_account')

@auth_bp.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('token', None)
    return redirect('/')



@auth_bp.route("/auth/callback")
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['token'] = token
    user = get_user_by_email(user_info.get('email'))
    if user is None:
        user = create_user(user_info.get('name'), user_info.get('email'), user_info.get('picture'))
        session['user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'picture': user_info.get('picture')
        }
        return redirect('/')

    session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'picture': user_info.get('picture')
    }
    return redirect('/')
