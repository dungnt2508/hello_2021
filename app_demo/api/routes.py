from flask import Blueprint, render_template
from .models import User, Customer, Invoice, Settings, Funds


bp_page = Blueprint('page',__name__, url_prefix='/page')
bp_user = Blueprint('user',__name__, url_prefix='/user')
bp_customer = Blueprint('customer',__name__, url_prefix='/customer')
bp_invoice = Blueprint('invoice',__name__, url_prefix='/invoice')
bp_setting = Blueprint('setting',__name__, url_prefix='/setting')
bp_funds = Blueprint('funds',__name__, url_prefix='/funds')


@bp_user.before_app_request
# @bp_page.before_app_request
# @bp_customer.before_app_request
# @bp_invoice.before_app_request
# @bp_setting.before_app_request
# @bp_funds.before_app_request
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

@bp_invoice.route('/filter/expired', methods=['GET'])
def invoice_filter_expired():
    return Invoice().filter_expired()

@bp_invoice.route('/filter/over_expired', methods=['GET'])
def invoice_filter_over_expired():
    return Invoice().filter_over_expired()

@bp_invoice.route('/filter_one/<id>', methods=['GET'])
def invoice_filter_one(id):
    return Invoice().filter_one(id)


@bp_invoice.route('/create', methods=('GET','POST'))
def invoice_create():
    return Invoice().create()


@bp_invoice.route('/pay', methods=('GET','POST'))
def invoice_pay():
    return Invoice().pay()

@bp_invoice.route('/pay/<id>', methods=('GET','POST'))
def invoice_pay_id(id):
    return Invoice().pay_id(id)


@bp_invoice.route('/redeem', methods=('GET','POST'))
def invoice_redeem():
    return Invoice().redeem()

@bp_invoice.route('/redeem/<id>', methods=('GET','POST'))
def invoice_redeem_id(id):
    return Invoice().redeem_id(id)



@bp_setting.route('/get_rate_kind_item/<kind_item>', methods=['GET'])
def get_rate_kind_item(kind_item):
    return Settings().get_rate_kind_item(int(kind_item))

@bp_setting.route('/set_rule', methods=('GET','POST'))
def set_rule():
    return Settings().set_rules()

@bp_setting.route('/filter_rate', methods=('GET','POST'))
def filter_rate():
    return Settings().filter_rate()


@bp_setting.route('/set_rate/<id>',methods=('GET','POST'))
def set_rate(id):
    return Settings().set_rate(id)

@bp_setting.route('/update_rate/', methods=('GET','POST'))
def update_rate():
    return Settings().update_rate()


@bp_funds.route('/collect', methods=('GET','POST'))
def collect():
    return Funds().collect()


@bp_funds.route('/spent', methods=('GET','POST'))
def spent():
    return Funds().spent()


@bp_funds.route('/filter', methods=('GET','POST'))
def funds_filter():
    return Funds().filter()