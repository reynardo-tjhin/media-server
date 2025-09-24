from flask import (
    Blueprint, render_template, url_for, request, g, session
)
from src.db import get_db

bp = Blueprint('movies', __name__, url_prefix='/movies')

@bp.route("/", methods=["GET"])
def home():

    print(request.args)

    # search is not empty
    movie_name = ""
    if (request.args.get("movie-name")):
        movie_name = request.args.get("movie-name")

    # dictionary of imdb_ratings
    imdb_ratings = {
        "Show All": -1,
        "8+ (Excellent)": 8,
        "7+ (Good)": 7,
        "6+ (Fair)": 6,
        "5+ (Average)": 5,
    }
    imdb_rating = -1
    imdb_rating_text = "Any IMDb Rating"
    if (request.args.get("imdb_rating")):
        imdb_rating = imdb_ratings.get(request.args.get("imdb_rating"))
        imdb_rating_text = request.args.get("imdb_rating")

    # get the db
    db = get_db()

    # filter by genre
    genres = db.execute('SELECT * FROM genre;').fetchall()
    valid_genre_ids = []
    genres_selected = request.args.getlist('genre')
    genres_final = []
    for genre in genres:
        if genre[1] in genres_selected:
            genres_final.append({
                'id': genre[0],
                'name': genre[1],
                'checked': 'checked',
            })
            valid_genre_ids.append(genre[0])
        else:
            genres_final.append({
                'id': genre[0],
                'name': genre[1],
                'checked': '',
            })

    # get the movies filtered by genre
    genre_id_query = ", ".join("?" for _ in range(len(valid_genre_ids)))
    if (len(valid_genre_ids) > 0):
        movies = db.execute(
            f'SELECT c.id, c.poster_location, c.name, '
            f'       c.imdb_rating, c.rotten_tomatoes_rating, c.metacritic_rating, '
            f'       c.release_year, c.genres '
            f'FROM ('
            f'  SELECT m.id, m.poster_location, m.name, '
            f'         m.imdb_rating, m.rotten_tomatoes_rating, m.metacritic_rating, '
            f'         strftime("%Y", m.release_date) AS release_year, '
            f'         GROUP_CONCAT(g.name, ", ") AS genres'
            f'  FROM movie AS m '
            f'    LEFT JOIN movie_genre AS mg ON m.id = mg.movie_id '
            f'    LEFT JOIN genre AS g ON mg.genre_id = g.id '
            f'  WHERE g.id IN ({genre_id_query})'
            f'        AND m.imdb_rating > ? '
            f'  GROUP BY m.id '
            f'  HAVING COUNT(DISTINCT g.id) = ?'
            f') AS c '
            f'  LEFT JOIN movie_genre AS mg ON c.id = mg.movie_id '
            f'  LEFT JOIN genre AS g ON g.id = mg.genre_id '
            f'GROUP BY c.id ', (*valid_genre_ids, imdb_rating, len(valid_genre_ids),)
        ).fetchall()

    # get the movies normally
    else:
        movies = db.execute(
            'SELECT m.id, m.poster_location, m.name, '
            '       m.imdb_rating, m.rotten_tomatoes_rating, m.metacritic_rating, '
            '       strftime("%Y", m.release_date) AS release_year, '
            '       GROUP_CONCAT(g.name, ", ") AS genres '
            'FROM movie AS m '
            '  LEFT JOIN movie_genre AS mg ON m.id = mg.movie_id '
            '  LEFT JOIN genre AS g ON mg.genre_id = g.id '
            'WHERE m.name LIKE ? '
            '      AND m.imdb_rating > ? '
            'GROUP BY m.id;', ('%'+movie_name+'%', imdb_rating,)
        ).fetchall()

    return render_template("movies/home.jinja2",
                           movie_name=movie_name,
                           movies=movies,
                           genres=genres_final,
                           genres_selected=genres_selected,
                           imdb_rating_text=imdb_rating_text)