from flask import (
    Blueprint, render_template, url_for, request, g, session
)
from src.db import get_db

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route("/", methods=["GET"])
def home():

    # search is not empty
    movie_name = ""
    if (request.args.get("movie-name")):
        movie_name = request.args.get("movie-name")

    # get the movies
    db = get_db()
    movies = db.execute(
        'SELECT m.id, m.poster_location, m.name, '
        '       m.imdb_rating, m.rotten_tomatoes_rating, m.metacritic_rating, '
        '       strftime("%Y", m.release_date) AS release_year, '
        '       GROUP_CONCAT(g.name, ", ") AS genres '
        'FROM movie AS m '
        '  LEFT JOIN movie_genre AS mg ON m.id = mg.movie_id '
        '  LEFT JOIN genre AS g ON mg.genre_id = g.id '
        'WHERE m.name LIKE ? '
        'GROUP BY m.id;', ('%'+movie_name+'%',)
    ).fetchall()

    # filter by genre
    genres = db.execute('SELECT * FROM genre;').fetchall()
    genres_selected = []
    genres_final = []
    for genre in genres:
        if genre[1] in request.args.getlist('genre'):
            genres_final.append({
                'id': genre[0],
                'name': genre[1],
                'checked': 'checked',
            })
            genres_selected.append(genre[1])
        else:
            genres_final.append({
                'id': genre[0],
                'name': genre[1],
                'checked': '',
            })

    return render_template("movies/home.jinja2",
                           movies=movies,
                           genres=genres_final,
                           genres_selected=genres_selected,)