import os
from flask import Flask
from flask import render_template
from flaskApp import db, auth, blog, simple_pages
from flaskApp.context_processors import utility_text_processors
from werkzeug.exceptions import NotFound
from flask_bootstrap import Bootstrap5

def page_not_found(e):
    return render_template("404.html"),404

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    db.init_app(app)
    # apply the blueprints to the app
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(simple_pages.bp)
    app.register_error_handler(404, page_not_found)
    bootstrap = Bootstrap5(app)
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'minty'


    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")
    app.context_processor(utility_text_processors)


    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    return app


app = create_app()