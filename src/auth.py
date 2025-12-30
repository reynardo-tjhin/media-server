import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash

from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/login', methods=["GET", "POST"])
def login():
    """
    Send the templated. Another function will check for login details
    """
    # already logged in
    if (session.get("user_id") != None):
        return redirect(url_for("home.home"))

    # otherwise
    return render_template('login.html')



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
        
        # check against the database
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if (user is None):
            error = "Username does not exist"
            return jsonify({
                "status": "FAIL",
                "message": error,
            })

        if (not check_password_hash(user['password'], password)):
            error = "Password is incorrect"
            return jsonify({
                "status": "FAIL",
                "message": error,
            })

        print("got here")

        session.clear()
        session['user_id'] = user['id']
        session['is_admin'] = bool(user['is_admin'])
        print(session)
        return jsonify({
            "status": "SUCCESS",
            "message": "successfully signed in",
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
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
