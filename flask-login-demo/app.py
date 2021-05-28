from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(port=5000)