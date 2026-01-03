import os

from flask import Blueprint, send_from_directory, current_app

bp = Blueprint("media", __name__, url_prefix='/media')


# route to serve a the poster image from the poster forlder
@bp.route("/<string:filename>")
def get_poster(filename):
    path = current_app.config['POSTERS_PATH']    
    return send_from_directory(
        path, filename
    )