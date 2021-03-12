from flask import Blueprint, render_template
from .models import User, Customer, Invoice, Settings, Funds


bp_page = Blueprint('page',__name__, url_prefix='/page')
bp_user = Blueprint('user',__name__, url_prefix='/user')
bp_customer = Blueprint('customer',__name__, url_prefix='/customer')
bp_invoice = Blueprint('invoice',__name__, url_prefix='/invoice')
bp_setting = Blueprint('setting',__name__, url_prefix='/setting')
bp_funds = Blueprint('funds',__name__, url_prefix='/funds')


@bp_user.before_app_request
@bp_page.before_app_request
@bp_customer.before_app_request
@bp_invoice.before_app_request
@bp_setting.before_app_request
@bp_funds.before_app_request
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


@bp_user.route('/create/<int:type>', methods=('GET','POST'))
def create(type):
    """

    :param type: 1 : NHÂN VIÊN / 2 : KHÁCH HÀNG
    :return:
    """
    return User().create(type)


@bp_page.route('/invoice/<int:type>', methods=('GET','POST'))
def invoice(type):
    """

    :param type: 1 : Vay / 2 : Mua / 3: Bán / 4 : Chuộc / 5 : TT lãi
    :return:
    """
    return User().invoice(type)


@bp_page.route('/dashboard', methods=['GET'])
def dashboard():
    return User().dashboard()


@bp_user.route('/filter', methods=['GET'])
def filter():
    return User().filter()


@bp_user.route('/filter_one/<email>', methods=['GET'])
def filter_one(email):
    return User().filter_one(email)


@bp_page.route('/qlkhachhang', methods=['GET'])
def qlkhachhang():
    return User().qlkhachhang()


@bp_customer.route('/filter', methods=['GET'])
def customer_filter():
    return Customer().filter()


@bp_customer.route('/filter_one/<email>', methods=['GET'])
def customer_filter_one(email):
    return Customer().filter_one(email)


@bp_invoice.route('/filter', methods=['GET'])
def invoice_filter():
    return Invoice().filter()


@bp_invoice.route('/create', methods=('GET','POST'))
def invoice_create():
    return Invoice().create()


@bp_setting.route('/get_rate/<kind_item>', methods=['GET'])
def get_rate(kind_item):
    return Settings().get_rate(int(kind_item))


@bp_funds.route('/collect', methods=('GET','POST'))
def collect():
    return Funds().collect()


@bp_funds.route('/spent', methods=('GET','POST'))
def spent():
    return Funds().spent()