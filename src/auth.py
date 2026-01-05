import functools

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/login', methods=["GET"])
def login():
    """
    Send the template. Another function will check for login details
    """
    # already logged in
    if (session.get("user_id") != None):
        return redirect(url_for("home.home"))

    # otherwise
    return render_template('login.html')



@bp.route('/signup', methods=["GET"])
def signup():
    """
    Send the template. Another function will check for sign up details
    """
    # already logged in
    if (session.get("user_id") != None):
        return redirect(url_for("home.home"))

    # otherwise
    return render_template('signup.html')



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))



@bp.route('/check-sigin', methods=["POST"])
def check_signin_details() -> str | None:
    """
    Check sign in details. Return error message or None.
    """
    error = None
    if (request.method == "POST"):
        # get the data
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        # get database
        db = get_db()
        
        # validation 1: user must exist
        user = db.execute("SELECT * FROM user WHERE username = ?;", (username,)).fetchone()
        if (user is None):
            error = "Username does not exist"
            return jsonify({
                "status": "FAIL",
                "message": error,
            })

        # validation 2: passwords must match
        if (not check_password_hash(user['password'], password)):
            error = "Password is incorrect"
            return jsonify({
                "status": "FAIL",
                "message": error,
            })

        session.clear()
        session['user_id'] = user['id']
        session['is_admin'] = True if user['is_admin'] == 'True' else False
        return jsonify({
            "status": "SUCCESS",
            "message": "successfully signed in",
        })
        


@bp.route('/check-signup', methods=['POST'])
def check_signup_details() -> str | None:
    """
    An API to check sign up details
    """
    if (request.method == "POST"):
        # get the data
        data = request.get_json()
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # get db
        db = get_db()
        
        # validation 1: no same username
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if (user is not None):
            error = "Username already exists. Please use another one."
            return jsonify({
                "status": "FAIL",
                "message": error,
            })
            
        # validation 2: password1 and password2 have to be the same
        if (password1 != password2):
            error = "Passwords are different."
            return jsonify({
                "status": "FAIL",
                "message": error,
            })
            
        # validation 3: if password length is less than 8
        if (len(password1) < 8):
            error = "Password is too short. It has to be greater than 8 characters."
            return jsonify({
                "status": "FAIL",
                "message": error
            })
            
        # passes all validations
        user_id = str(uuid4())
        db.execute(
            "INSERT INTO user (id, username, password, is_admin) VALUES (?, ?, ?, ?);",
            (user_id, username, generate_password_hash(password1), "False",)
        )
        db.commit()
        session.clear()
        session['user_id'] = user_id
        session['is_admin'] = False
        return jsonify({
            "status": "SUCCESS",
            "message": "user successfully added",
        })



@bp.route('/username', methods=["GET"])
def get_username():
    """
    An API to get the username
    """
    if (session.get('user_id') is not None):
        db = get_db()
        user = db.execute("SELECT username FROM user WHERE id = ?;", (session.get('user_id'),)).fetchone()
        return jsonify({
            "status": "SUCCESS",
            "message": user[0],
        })
    return jsonify({
        "status": "FAIL",
        "message": "not signed in",
    })



@bp.route('/is-logged-in', methods=["GET"])
def is_logged_in():
    """
    An API to check whether the user is logged in
    """
    if (session.get('user_id') is not None):
        return jsonify({
            "status": "SUCCESS",
            "message": "True",
        })
    return jsonify({
        "status": "SUCCESS",
        "message": "False",
    })



@bp.route('/is-admin', methods=["GET"])
def is_admin():
    """
    An API to check whether the user logged in is an admin
    """
    if (session.get('user_id') is None):
        return jsonify({
            "status": "SUCCESS",
            "message": "Not logged in",
        })
    if (session.get("is_admin") is not None):
        if (session.get("is_admin")):
            return jsonify({
                "status": "SUCCESS",
                "message": "True",
            })
        return jsonify({
            "status": "SUCCESS",
            "message": "False",
        })
    return jsonify({
        "status": "SUCCESS",
        "message": "Error: server error",
    })



@bp.before_app_request
def load_logged_in_user():
    """
    Checks if user is logged in based on sessions.
    If logged in, set g variable of flask to be the user.
    """
    user_id = session.get('user_id')
    
    if (user_id is None):
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



# TODO: if not admin, reroute to 405 not authorized
def admin_required(view):
    """
    Checks if user is admin. If not admin, will require login
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or not session.get('is_admin'):
            return redirect(url_for('home.unauthorized'))
        return view(**kwargs)
    return wrapped_view
