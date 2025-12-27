import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash

from src.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/login', methods=["GET", "POST"])
def login():
    # already logged in
    if (session.get("user_id") != None and session.get("is_admin") == True):
        return redirect(url_for("admin.home"))

    # logging in
    if (request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        error = None

        # get user
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # check password
        # the first paramater for check_password_hash: pwhash
        # which is the already hashed password
        # the method will hash the current password and compare against the hashed
        if not check_password_hash(user['password'], password):
            error = "Password is incorrect."

        if (error is None and user['is_admin'] == "True"):

            # session is a dict that stores data across requests.
            # when validation succeeds, boolean is stored in a new sesion.
            # the data is stored in a cookie that is sent to the browser,
            # and the browser then sends it back with subsequent requests.
            # Flask securely signs the that it can't be tampered with.
            session.clear()
            session['user_id'] = user['id']
            session['is_admin'] = True
            return redirect(url_for("admin.home"))
        
        elif (error is None and user['is_admin'] == "False"):
            session.clear()
            session['user_id'] = user['id']
            session['is_admin'] = False
            return redirect(url_for('home.home'))
        
        flash(error)

    return render_template('login.html')



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))



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
