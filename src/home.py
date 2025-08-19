import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import (check_password_hash)
from src.db import get_db

# create a blueprint (like a factory method)
# registered in __init__.py
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('home.html')
