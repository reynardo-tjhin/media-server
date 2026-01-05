import os

from flask import Blueprint, send_from_directory, current_app

bp = Blueprint("media", __name__, url_prefix='/media')


# route to serve the poster image from the posters forlder
@bp.route("/poster/<string:filename>")
def get_poster(filename):
    path = current_app.config['POSTERS_PATH']    
    return send_from_directory(
        path, filename
    )

# route to serve the banner image from the banners folder
@bp.route("/banner/<string:filename>")
def get_banner(filename):
    path = current_app.config['BANNERS_PATH']
    return send_from_directory(
        path, filename
    )
    
# route to serve the movies file from the movies folder
# @bp.route("")