import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from . import home, db, admin, auth

csrf = CSRFProtect()

def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.
    """
    # create the app object
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overwritten by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "src.sqlite"),
    )

    if (test_config is None):
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test conig if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # register blueprints
    app.register_blueprint(home.bp)
    # app.register_blueprint(movies.bp)
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(auth.bp, url_prefix="/auth")

    # register database
    db.init_app(app=app)

    # register CSRF Protection
    csrf.init_app(app=app)
    
    # make url_for("index") == url_for("blog.index")
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial, the blog will be the main index
    # app.add_url_rule("/", endpoint="index")

    return app