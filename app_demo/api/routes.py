from flask import Blueprint, render_template
from .models import User

bp = Blueprint('auth',__name__, url_prefix='/auth')
bp_page = Blueprint('page',__name__, url_prefix='/page')


@bp.before_app_request
@bp_page.before_app_request
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


@bp_page.route('/dashboard', methods=['GET'])
def dashboard():
    return User().dashboard()


@bp_page.route('/qlnhanvien', methods=['GET'])
def qlnhanvien():
    return User().qlnhanvien()


@bp_page.route('/qlkhachhang', methods=['GET'])
def qlkhachhang():
    return User().qlkhachhang()