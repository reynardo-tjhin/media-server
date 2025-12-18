import re

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from uuid import uuid4

from src.auth import admin_required
from src.db import get_db
from typing import Any

bp = Blueprint('admin', __name__, url_prefix='/admin')



@bp.route("/")
@admin_required
def home():
    """
    Admin dashboard: Read operation on various tables
    """
    db = get_db()

    # get basic information
    movies_count = db.execute('SELECT COUNT(DISTINCT m.id) FROM movie AS m;').fetchone()
    users_count = db.execute('SELECT COUNT(DISTINCT u.id) FROM user AS u;').fetchone()
    genres_count = db.execute('SELECT COUNT(DISTINCT g.id) FROM genre AS g;').fetchone()

    # get the first three movies
    movies = db.execute('SELECT * FROM movie LIMIT 3;').fetchall()
    customised_movies = [
        {
            **dict(movie),
            'name': movie['name'],
            'description': movie['description'][:60] + "...",
            'imdb_rating': movie['imdb_rating'],
            'release_date': movie['release_date'],
            'media_location': movie['media_location'],
            'duration': movie['duration'],
        }
        for movie in movies
    ]

    # get all the genres name
    genres = db.execute('SELECT id, name FROM genre;').fetchall()

    # return by rendering the template
    return render_template("admin/admin_dashboard.html",
                           movies_count=movies_count[0],
                           users_count=users_count[0],
                           genres_count=genres_count[0],
                           movies=customised_movies,
                           genres=genres,)



@bp.route("/movies")
@admin_required
def movies():
    """
    Movies dashboard for admin: to create, read, update and delete movies
    CREATE, UPDATE and DELETE movies use different functions
    This function only focuses on read operations
    """
    # search as the query parameter
    search_movie_by_name = ''
    if (request.args.get('search')):
        search_movie_by_name = request.args['search']
    
    # get all the movies data
    db = get_db()
    movies = db.execute(
        'SELECT '
        '   m.*, '
        '   COALESCE(GROUP_CONCAT(g.name, ", "), "No genres") AS genres '
        'FROM movie AS m '
        'LEFT OUTER JOIN movie_genre AS mg ON m.id = mg.movie_id '
        'LEFT OUTER JOIN genre AS g ON g.id = mg.genre_id '
        'WHERE m.name LIKE ? '
        'GROUP BY m.id;', ('%'+search_movie_by_name+'%',)
        # f'ORDER BY {sort_by_dict[sort_by]};', ('%'+search_movie_by_name+'%',)
    ).fetchall()

    # get all the genres data - not going to be included in movie_genres for readability
    genres = db.execute('SELECT id, name FROM genre;').fetchall()
    return render_template("admin/movies.html", 
                           movies=movies,
                           genres=genres,)



@bp.route('/add-movie', methods=["GET", "POST"])
@admin_required
def add_movie():
    """
    A CREATE operation to create a new movie and add to the database
    """
    if (request.method == "POST"):
        
        # get the post data
        movie_name = request.form['movieName']
        movie_description = request.form['movieDescription']
        imdb_rating = request.form['imdbRating']
        rotten_tomatoes_rating = request.form['rottenTomatoesRating']
        metacritic_rating = request.form['metacriticRating']
        release_date = request.form['releaseDate']
        media_location = request.form['mediaLocation']
        poster_location = request.form['posterLocation']
        duration = request.form['duration']
        
        # validations
        error = _validate_movie_entries(request.form)
        if (error):
            flash(error)
            return redirect(url_for('admin.movies'))
        
        # add the movie to database
        db = get_db()
        movie_id = str(uuid4())
        db.execute(
            'INSERT INTO movie (id, name, description, imdb_rating, rotten_tomatoes_rating, metacritic_rating, release_date, media_location, poster_location, duration)'
            ' VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (movie_id, movie_name, movie_description, imdb_rating, rotten_tomatoes_rating, metacritic_rating, release_date, media_location, poster_location, duration,)
        )
        db.commit()
        
        # add the checked genre to genres
        genres = db.execute("SELECT * FROM genre;").fetchall()
        for genre in genres:
            # genre was checked, add to database
            if (genre['id'] in request.form.keys()):
                db.execute('INSERT INTO movie_genre (movie_id, genre_id) VALUES(?, ?)', (movie_id, genre['id'],))
                db.commit()
        
    return redirect(url_for('admin.movies'))



@bp.route('/delete-movie/<string:movie_id>', methods=["POST"])
@admin_required
def delete_movie(movie_id: str):
    """
    A DELETE operation to delete the movie based on the id
    """
    # requires admin login
    # returns a 404 if movie_id does not exist
    get_movie(movie_id)

    # delete the movie from database
    db = get_db()
    db.execute('DELETE FROM movie WHERE id = ?', (movie_id,))
    db.commit()

    return redirect(url_for('admin.movies'))



@bp.route('/update-movie/<string:movie_id>', methods=["POST"])
@admin_required
def update_movie(movie_id: str):
    """
    Update the movie data according to the movie id
    """
    if (request.method == "POST"):
        # get the json data from the request
        data = request.get_json()
        
        # get the error
        error = _validate_movie_entries(data, movie_id=movie_id)
        if (error != None):
            return jsonify({
                "status": "FAIL",
                "message": error,
            })
        
        # get the individual data from the request
        movie_name = data['movieName']
        movie_description = data['movieDescription']
        imdb_rating = data['imdbRating']
        rotten_tomatoes_rating = data['rottenTomatoesRating']
        metacritic_rating = data['metacriticRating']
        release_date = data['releaseDate']
        media_location = data['mediaLocation']
        poster_location = data['posterLocation']
        duration = data['duration']
        
    
    return jsonify({
        "status": "SUCCESS",
        "message": "ok",
    })


@bp.route('/edit-movie/<string:movie_id>', methods=["GET", "POST"])
@admin_required
def edit_movie(movie_id: str):
    """
    Add a new movie or update the details of an existing movie.
    """
    if (request.method == "POST"):
        # get the post data
        movie_name = request.form['movieName']
        movie_description = request.form['movieDescription']
        imdb_rating = request.form['imdbRating']
        rotten_tomatoes_rating = request.form['rottenTomatoesRating']
        metacritic_rating = request.form['metacriticRating']
        release_date = request.form['releaseDate']
        media_location = request.form['mediaLocation']
        poster_location = request.form['posterLocation']
        duration = request.form['duration']
        
        print(request.form.keys())
        
        # validations
        error = _validate_movie_entries(request.form, movie_id=movie_id)
        if (error):
            flash(error)
            return redirect(url_for('admin.movies'))

        # no error
        # db = get_db()
        # db.execute(
        #     'UPDATE movie SET name = ?, description = ?, imdb_rating = ?,'
        #     ' rotten_tomatoes_rating = ?, metacritic_rating = ?, release_date = ?,'
        #     ' media_location = ?, poster_location = ? , duration = duration WHERE id = ?', (movie_name, movie_description, imdb_rating, rotten_tomatoes_rating, metacritic_rating, release_date, media_location, poster_location, duration, movie_id,)
        # )
        # db.commit()
        
        # update the genres
        # genres = db.execute("SELECT * FROM genre;").fetchall()
        # for genre in genres:
        #     # an existing genre needs to be deleted
        #     if (genre['id'] not in request.form.keys() and genre['checked'] == 'checked'):
        #         db.execute(
        #             'DELETE FROM movie_genre'
        #             ' WHERE movie_id = ? AND genre_id = ?', (movie_id, genre['id'],)
        #         )
        #         db.commit()
        #     # a new genre needs to be added
        #     elif (genre['id'] in request.form.keys() and genre['checked'] == ''):
        #         db.execute(
        #             'INSERT INTO movie_genre (movie_id, genre_id)'
        #             ' VALUES(?, ?);', (movie_id, genre['id'],)
        #         )
        #         db.commit()
            
    return redirect(url_for('admin.movies'))



@bp.route('/<string:genre_id>')
@admin_required
def genre(genre_id: str):
    # define columns to show and its style
    table_columns = [
        {'key': 'id', 'label': 'ID', 'width': '50px'},
        {'key': 'name', 'label': 'Name', 'width': '150px'},
        {'key': 'description', 'label': 'Description', 'width': '300px'},
        {'key': 'imdb_rating', 'label': 'IMDB', 'width': '80px'},
        {'key': 'rotten_tomatoes_rating', 'label': 'RT', 'width': '80px'},
        {'key': 'metacritic_rating', 'label': 'Metacritic', 'width': '80px'},
        {'key': 'release_date', 'label': 'Release Date', 'width': '100px'},
        {'key': 'media_location', 'label': 'Media Location', 'width': '200px'},
        {'key': 'delete', 'label': 'Delete', 'width': '80px'},
        {'key': 'update', 'label': 'Update', 'width': '80px'},
    ]

    # get the movies data that have the specific genre
    db = get_db()
    genre = db.execute('SELECT * from genre where id = ?', (genre_id,)).fetchone()
    movies = db.execute(
        'SELECT m.* '
        'FROM movie AS m '
        'JOIN movie_genre AS mg ON m.id = mg.movie_id '
        'WHERE mg.genre_id = ?', (genre_id,)
    ).fetchall()

    # no movies shown
    style = "display: none;"
    if (len(movies) <= 0):
        style = "display: block;"

    return render_template("admin/genre.jinja2",
                           genre=genre,
                           movies=movies,
                           table_columns=table_columns,
                           style=style,)



@bp.route('/delete-genre/<string:genre_id>', methods=["POST"])
@admin_required
def delete_genre(genre_id: str):
    # returns a 404 if genre_id does not exist
    get_genre(genre_id)

    # delete the genre from database
    db = get_db()
    db.execute('DELETE FROM genre WHERE id = ?', (genre_id,))
    db.commit()

    return redirect(url_for('admin.movies'))



@bp.route('/edit-genre', methods=["GET", "POST"])
@admin_required
def edit_genre():
    genre = None
    if (request.args['action'] == 'update'):
        db = get_db()
        genre = db.execute(
            'SELECT * FROM genre WHERE id = ?', (request.args['genre_id'],)
        ).fetchone()
    
    if (request.method == "POST"):
        genre_name = genre['name'] if genre else request.form['genreName']
        genre_description = request.form['genreDescription']
        error = None

        # validation not empty
        if (not genre_name):
            error = "Genre Name is required."
        if (not genre_description):
            error = "Genre Description is required."
        
        # check if genre_name already exists in database
        db = get_db()
        if (genre_name and request.args['action'] == 'add'):
            genre = db.execute(
                'SELECT * FROM genre WHERE name = ?', (genre_name.capitalize(),)
            ).fetchone()
            if (genre):
                error = "Genre Name already exists."
                genre = None
        
        # after validation, no errors
        if (error is None):
            if (request.args['action'] == 'update'):
                db.execute(
                    'UPDATE genre SET description = ? WHERE id = ?;', (genre_description, genre['id'],)
                )
                db.commit()
            else:
                genre_id = str(uuid4())
                db.execute(
                    'INSERT INTO genre (id, name, description) VALUES (?, ?, ?)', (genre_id, genre_name.capitalize(), genre_description)
                )
                db.commit()
            return redirect(url_for('admin.movies'))
        
        flash(error)

    return render_template("admin/edit_genre.jinja2",
                           genre=genre,
                           action=request.args['action'],)



# ================================================
# HELPER FUNCTIONS
# ================================================
def get_movie(movie_id: str) -> Any:
    """
    Check if movie_id exists. If not exists, return with 404.
    """
    movie = get_db().execute(
        'SELECT * FROM movie WHERE id = ?', (movie_id,)
    ).fetchone()

    if movie is None:
        abort(404, f"Movie ID {movie_id} does not exist.")

    return movie

def get_genre(genre_id: str) -> Any:
    """
    Check if genre_id exists. If not exists, return with 404.
    """
    genre = get_db().execute(
        'SELECT * FROM genre WHERE id = ?', (genre_id,)
    ).fetchone()

    if genre is None:
        abort(404, f"Genre ID {genre_id} does not exist.")
    
    return genre

def _validate_movie_entries(movie_data: dict[str, Any], movie_id: str = None) -> str | None:
    """
    If no errors, return None.
    If there is an error(s), return the first error found.
    
    Returns the error string.
    """
    # initialise the variable 'error' (to be returned)
    error = None
    
    # get the database
    db = get_db()
    
    # get the movie data
    movie_name = movie_data['movieName']
    movie_description = movie_data['movieDescription']
    imdb_rating = movie_data['imdbRating']
    rotten_tomatoes_rating = movie_data['rottenTomatoesRating']
    metacritic_rating = movie_data['metacriticRating']
    release_date = movie_data['releaseDate']
    media_location = movie_data['mediaLocation']
    poster_location = movie_data['posterLocation']
    duration = movie_data['duration']
    
    # validation 1: the below data are all required
    if not movie_name:
        error = "Movie Name is required."
        return error
    
    elif not movie_description:
        error = "Movie Description is required."
        return error
    
    elif not release_date:
        error = "Release Date is required."
        return error
    
    elif not media_location:
        error = "Media Location is required."
        return error

    elif not poster_location:
        error = "Poster Location is required."
        return error

    # validation 2: no two movie names exists
    name = db.execute('SELECT name FROM movie WHERE name = ?', (movie_name,)).fetchone()
    if (movie_id is not None):
        prev_name = db.execute('SELECT name FROM movie WHERE id = ?', (movie_id,)).fetchone()
        # the name is updated but the updated name already exists in database
        if (prev_name[0] != movie_name and name is not None):
            error = "Movie name already exists"
            return error
    else:
        if (name is not None):
            error = "Movie name already exists."
            return error
    
    # validation 3: no two media locations is the same
    loc = db.execute('SELECT media_location FROM movie WHERE media_location = ?', (media_location,)).fetchone()
    if (loc is not None):
        error = "Media location already exists. New movie cannot be from the same existing media location."
        return error

    # validation 3: both metacritic rating and rotten tomatoes rating need to be from 0 to 100
    pattern = r'^(100|[1-9]?[0-9])$'
    if (rotten_tomatoes_rating):
        if not bool(re.match(pattern, rotten_tomatoes_rating)):
            error = "Rotten Tomatoes Rating should be from 0 to 100."
            return error
    
    if (metacritic_rating):
        if not bool(re.match(pattern, metacritic_rating)):
            error = "Metacritic Rating should be from 0 to 100."
            return error

    # validation 4: imdb rating needs to be from 0.0 to 10.0
    pattern = r'^(10\.0|[0-9]\.[0-9])$'
    if (imdb_rating):
        if not bool(re.match(pattern, imdb_rating)):
            error = "IMDb Rating should be from 0.0 to 10.0 (strictly only 1 decimal place)."
            return error

    if (duration):
        if (not duration.isnumeric()):
            error = "Duration needs to be a number"
            return error

    return error