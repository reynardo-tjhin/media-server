import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from . import home, db, admin, auth, movies, media
from .config import config

# initialise csrf object for secure post method
csrf = CSRFProtect()

def create_app():
    """
    Create and configure an instance of the Flask application.
    """
    # detemine the config based on environment variable
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # create the app object
    app = Flask(__name__)

    # load the configuration
    cfg = config[config_name]
    app.config.from_object(cfg)
    
    # update the database instance path
    app.config.update(DATABASE=os.path.join(app.instance_path, 'src.sqlite'))
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # register blueprints
    app.register_blueprint(home.bp)
    app.register_blueprint(admin.bp, url_prefix="/admin")
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(movies.bp, url_prefix="/movies")
    app.register_blueprint(media.bp, url_prefix="/media")

    # register database
    db.init_app(app=app)

    # register CSRF Protection
    csrf.init_app(app=app)
    
    # make url_for("index") == url_for("blog.index")
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial, the blog will be the main index
    # app.add_url_rule("/", endpoint="index")
    
    # handle errors
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("status_404.html"), 404
    
    @app.errorhandler(403)
    def page_not_authorized(error):
        return render_template("status_403.html"), 403

    return app