from flask import Flask, render_template, session, request, send_file
import hashlib
import os
import requests
from io import BytesIO
from authlib.integrations.flask_client import OAuth
from routes.auth import auth_bp, oauth
from routes.google_drive import google_bp
from routes.todos import todo_bp
from db.database import Base, engine
from db.todo_crud import get_all_todos


app = Flask(__name__)
app.secret_key = hashlib.sha256(os.urandom(1024)).hexdigest()

oauth.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(todo_bp, url_prefix='/todo')
app.register_blueprint(google_bp)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind = engine)


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email",  
    "https://www.googleapis.com/auth/userinfo.profile"   
]

CACHE_DIR = "image_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/proxy_image')
def proxy_image():
    image_url = request.args.get('url')
    if not image_url:
        return "URL no especificada", 400

    # Generar un nombre de archivo basado en la URL
    image_filename = os.path.join(CACHE_DIR, image_url.split('/')[-1])

    # Si la imagen ya está en caché, devolverla directamente
    if os.path.exists(image_filename):
        return send_file(image_filename, mimetype="image/jpeg")

    try:
        # Solicitar la imagen al servidor remoto
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Guardar la imagen en caché
        with open(image_filename, "wb") as f:
            f.write(response.content)

        return send_file(image_filename, mimetype=response.headers.get('Content-Type'))
    except requests.exceptions.RequestException:
        return "Error al cargar la imagen", 500

@app.route("/")
def home():
    user = session.get("user")
    if user:
        return render_template('welcome.html', user = user, todos=get_all_todos())
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000, debug = True)
