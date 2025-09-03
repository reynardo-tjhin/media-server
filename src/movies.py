from flask import (
    Blueprint, render_template, url_for, request, g, session
)
from src.db import get_db

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route("/")
def home():

    db = get_db()
    movies = db.execute(
        'SELECT name, description, imdb_rating, rotten_tomatoes_rating, metacritic_rating, release_date '
        'FROM movie;'
    ).fetchall()

    return render_template("movies/home.jinja2",
                           movies=movies,)