from flask import Flask, render_template, url_for, redirect, session
import hashlib
import os
from authlib.integrations.flask_client import OAuth
from routes.auth import auth_bp, oauth
from routes.todos import todo_bp
from db.database import Base, engine
from db.todo_crud import get_all_todos


app = Flask(__name__)
app.secret_key = hashlib.sha256(os.urandom(1024)).hexdigest()

oauth.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(todo_bp, url_prefix='/todo')

# Crear las tablas en la base de datos
Base.metadata.create_all(bind = engine)


SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",  
    "https://www.googleapis.com/auth/userinfo.profile"   
]


@app.route("/")
def home():
    user = session.get("user")
    todos = get_all_todos()
    if user:
        return render_template('welcome.html', user = user, todos=todos)
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)