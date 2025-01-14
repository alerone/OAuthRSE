from flask import flash, redirect, render_template, request, session, url_for, Blueprint
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def get_drive_service(credentials):
    return build("drive", "v3", credentials=credentials)


google_bp = Blueprint("google", __name__)


@google_bp.route("/search_photos", methods=["GET"])
def search_photos():
    if not "token" in session:
        return "There is no token"

    print('scope', session.get("token")) 

    credentials = Credentials(token=session.get("token")['access_token'])
    drive_service = get_drive_service(credentials)

    results = (
        drive_service.files()
        .list(
            q="mimeType contains 'image/'",
            pageSize=5,
            fields="files(id, name, webViewLink, thumbnailLink)",
        )
        .execute()
    )

    items = results.get("files", [])
    return render_template("search_photos.html", photos=items)


@google_bp.route("/select_photo", methods=["POST"])
def select_photo():
    photo_id = request.form.get("photo_id")
    if not photo_id:
        flash("No se seleccionó ninguna foto.", "error")
        return redirect(url_for("search_photos"))

    # Guarda el ID de la foto en la sesión
    session["selected_photo_id"] = photo_id
    flash("Foto seleccionada correctamente.", "success")
    return redirect(url_for("todo.create"))
