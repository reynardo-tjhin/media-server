from flask import (
    Blueprint, render_template, url_for, request, g, session
)
from src.db import get_db

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route("/", methods=["GET", "POST"])
def home():

    # search is not empty
    movie_name = ""
    if (request.args.get("movie-name")):
        movie_name = request.args.get("movie-name")

    # get the movies
    db = get_db()
    movies = db.execute(
        'SELECT m.poster_location, m.name, m.description, '
        '       m.imdb_rating, m.rotten_tomatoes_rating, m.metacritic_rating, '
        '       strftime("%e", m.release_date) || " " || '
        '       CASE strftime("%m", m.release_date) '
        '         WHEN "01" THEN "January" '
        '         WHEN "02" THEN "February" '
        '         WHEN "03" THEN "March" '
        '         WHEN "04" THEN "April" '
        '         WHEN "05" THEN "May" '
        '         WHEN "06" THEN "June" '
        '         WHEN "07" THEN "July" '
        '         WHEN "08" THEN "August" '
        '         WHEN "09" THEN "September" '
        '         WHEN "10" THEN "October" '
        '         WHEN "11" THEN "November" '
        '         WHEN "12" THEN "December" '
        '       END || " " || '
        '       strftime("%Y", m.release_date) AS release_date, '
        '       GROUP_CONCAT(g.name, ", ") AS genres '
        'FROM movie AS m '
        '  LEFT JOIN movie_genre AS mg ON m.id = mg.movie_id '
        '  LEFT JOIN genre AS g ON mg.genre_id = g.id '
        'WHERE m.name LIKE ? '
        'GROUP BY m.name;', ('%'+movie_name+'%',)
    ).fetchall()

    return render_template("movies/home.jinja2",
                           movies=movies,)