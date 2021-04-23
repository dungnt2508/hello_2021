from flask import Blueprint, render_template
from .models import User


bp_page = Blueprint('page',__name__, url_prefix='/page')
bp_user = Blueprint('user',__name__, url_prefix='/user')


@bp_user.before_app_request
def load_logged_in_user():
    User.load_logged_in_user()


@bp_user.route('/register', methods=('GET','POST'))
def register():
    return User().register()


@bp_user.route('/login', methods=('GET','POST'))
def login():
    return User().login()


@bp_user.route('/logout', methods=['GET'])
def logout():
    return User().logout()

@bp_page.route('/dashboard', methods=['GET'])
def dashboard():
    return User().dashboard()