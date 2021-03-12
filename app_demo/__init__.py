import os

from flask import Flask, render_template, session, redirect


def create_app(test_config=None):

    # create and configure the app
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build/templates')

    app = Flask(__name__,
                static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return render_template('user/login.html')

    from .api import routes
    app.register_blueprint(routes.bp_user)
    app.register_blueprint(routes.bp_customer)
    app.register_blueprint(routes.bp_invoice)
    app.register_blueprint(routes.bp_setting)
    app.register_blueprint(routes.bp_page)
    app.register_blueprint(routes.bp_funds)

    return app