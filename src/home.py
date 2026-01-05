from flask import Blueprint, render_template
from src.db import get_db

# create a blueprint (like a factory method)
# registered in __init__.py
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    # get the database pointer
    db = get_db()
    
    # get the 6 latest movies
    movies = db.execute('SELECT * FROM movie ORDER BY release_date DESC LIMIT 6;').fetchall()
    
    return render_template('home.html',
                           active_movie=movies[0],
                           movies=movies[1:],)


@bp.route('/403')
def unauthorized():
    return render_template('status_403.html')