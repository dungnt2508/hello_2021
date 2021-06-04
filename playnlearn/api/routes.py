from flask import Blueprint, render_template, request
from .models import User

bp = Blueprint('',__name__, url_prefix='/')
bp_user = Blueprint('user',__name__, url_prefix='/user')


@bp.route('/register', methods=('GET','POST'))
def register():
    return render_template('register.html')


@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        return render_template('register.html')
    return render_template('login.html')


@bp_user.route('/logout', methods=['GET'])
def logout():
    return 'logout'

