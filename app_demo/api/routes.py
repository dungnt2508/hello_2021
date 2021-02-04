from flask import Blueprint, render_template
from .models import User

bp = Blueprint('auth',__name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    User().load_logged_in_user()


@bp.route('/register', methods=('GET','POST'))
def register():
    return User().register()


@bp.route('/login', methods=('GET','POST'))
def login():
    return User().login()


@bp.route('/logout', methods=['GET'])
def logout():
    return User().logout()