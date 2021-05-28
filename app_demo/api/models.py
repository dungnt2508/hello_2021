from flask import Flask, jsonify, request, session, redirect, render_template, url_for, flash, g
from passlib.hash import pbkdf2_sha256
import uuid
import datetime as dt
from datetime import datetime
from datetime import date
import dateutil.parser
from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from app_demo.db import db
from instance.rule_name import create_user_name

class User:
    """
    User
    """

    @staticmethod
    def load_logged_in_user():
        """
            check user class

        :return:
        """
        user_id = session.get('id')
        # print(user_id)
        try:

            if user_id is None:
                g.user = None
            else:
                g.user = db.users.find_one({"_id": user_id}, {"password": 0, "_id": 0})

                g.settings = db.settings.find({"status": "1"}, {"_id": 0})
                g.total_invoice = 0
                if db.invoice.find(({})).count() > 0:
                    g.total_invoice = db.invoice.find().count()
                    g.invoices = db.invoice.find()
                g.total_customer = db.customers.find().count()
                g.customer = []
                if g.total_customer != 0:
                    g.customers = list(db.customers.aggregate([{"$sort": {"_id": -1}}]))[0]

                # get quĩ
                g.treasure = 0
                if db.funds.find_one():
                    g.treasure = "${:,.0f}".format(float(list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))[0]["funds"]))
                # print(g.settings)
                today = datetime.combine(date.today(), datetime.min.time())
                g.logs = list(db.logs.find({"date_created": {"$gte": today}}))
                # print(g.logs)
                # setting filter
                g.pipeline_filter_status = "[ { '$project': { '_id': 0, 'invoice_id': 1, 'item_kind': 1, 'item_name': 1, 'customer': 1, 'price_pawn': 1, 'rate': 1, 'price_rate': 1, 'from_date': 1, 'to_date': 1, 'user_created': 1, 'date_created': 1, 'status': 1, 'status_invoice': { '$switch': { 'branches': [ { 'case': { '$and': [ { '$gt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '0' }, { 'case': { '$and': [ { '$eq': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '1' }, { 'case': { '$and': [ { '$lt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '2' },{ 'case': { '$and': [ { '$eq': [ '1', '1' ] }, { '$in': [ '$status', [ 10, 10 ] ] } ] }, 'then': '10' } ], 'default': '-1' } } } },{ '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1,'status_invoice':1, 'status_invoice_msg':{ '$switch':{ 'branches':[ { 'case':{ '$eq':[ '$status_invoice', '0' ] }, 'then':'Đang giữ' }, { 'case':{ '$eq':[ '$status_invoice', '1' ] }, 'then':'Đến hạn' }, { 'case':{ '$eq':[ '$status_invoice', '2' ] }, 'then':'Quá hạn' },{ 'case':{ '$eq':[ '$status_invoice', '10' ] }, 'then':'Đã xóa' } ], 'default':'Đã tất toán' } } } }, { '$match': { 'status_invoice': '%s' } },{ '$lookup': {'from': 'settings', 'localField': 'item_kind', 'foreignField': 'kind_item', 'as': 'rate_invoice' }}, {'$sort':{'from_date':-1}} ]"
                g.pipeline_filter_all = "[ { '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1, 'status_invoice':{ '$switch':{ 'branches':[ { 'case':{ '$and':[ { '$gt':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'0' }, { 'case':{ '$and':[ { '$eq':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'1' }, { 'case':{ '$and':[ { '$lt':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'2' },{ 'case': { '$and': [ { '$eq': [ '1', '1' ] }, { '$in': [ '$status', [ 10, 10 ] ] } ] }, 'then': '10' } ], 'default':'-1' } } } }, { '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1, 'status_invoice_msg':{ '$switch':{ 'branches':[ { 'case':{ '$eq':[ '$status_invoice', '0' ] }, 'then':'Đang giữ' }, { 'case':{ '$eq':[ '$status_invoice', '1' ] }, 'then':'Đến hạn' }, { 'case':{ '$eq':[ '$status_invoice', '2' ] }, 'then':'Quá hạn' },{ 'case':{ '$eq':[ '$status_invoice', '10' ] }, 'then':'Đã xóa' } ], 'default':'Đã tất toán' } } } },{ '$lookup': {'from': 'settings', 'localField': 'item_kind', 'foreignField': 'kind_item', 'as': 'rate_invoice' }}, {'$sort':{'from_date':-1}} ]"

        except Exception as e:
            print(str(e))

    def register(self):
        """
            register user
        :return:
        """
        try:
            if request.method == 'POST':
                # Create the user object
                user_name = create_user_name(request.form.get("fullname"))
                count_user = db.users.find({"user_name": {"$regex": user_name}}).count()
                user = {
                    "_id": uuid.uuid4().hex,
                    "name": request.form.get("fullname"),
                    "user_name": user_name + str(count_user + 1),
                    "email": request.form.get("email"),
                    "password": request.form.get("password"),
                    "cmnd_1": request.form.get("cmnd_1"),
                    "cmnd_2": request.form.get("cmnd_2"),
                    "note": request.form.get("note"),
                    "is_admin": False
                }

                # Encrypt the password
                user["password"] = generate_password_hash(user["password"])

                # Check exists email
                if db.users.find_one({"email": user["email"]}):
                    return jsonify({"error": "Email address already in use"}), 400
                if db.users.insert_one(user):
                    Logs().insert_log(1, user)
                    session.clear()
                    session['name'] = user['name']
                    session['user_name'] = user['user_name']
                    session['id'] = str(user['_id'])
                    return jsonify(user), 200
        except Exception as e:
            print(str(e))

        return render_template('user/register.html')

    def login(self):
        """
            login
            :return:
        """
        try:
            if request.method == 'POST':
                user_name = request.form['user_name']
                password = request.form['password']
                error = None
                # print(user_name)
                if '@' in user_name:  # filter by email
                    user = db.users.find_one({'email': user_name})
                if '@' not in user_name:  # filter by user_name
                    user = db.users.find_one({'user_name': user_name})

                if user is None:
                    error = 'Incorrect username.'
                    return jsonify({"error": error}), 400
                elif not check_password_hash(user['password'], password):
                    error = 'Incorrect password.'
                    return jsonify({"error": error}), 400

                if error is None:
                    session.clear()
                    session['email'] = user['email']
                    session['user_name'] = user['user_name']
                    session['id'] = str(user['_id'])
                    # print(session)

                    return jsonify(user), 200

                flash(error)
        except Exception as e:
            print(str(e))
        return render_template('user/login.html')

    def logout(self):
        """
            logout
        :return:
        """
        try:
            session.clear()
        except Exception as e:
            print(str(e))
        return redirect("/")

    def create(self, type):
        """
            create
            :param type:
            :return:
        """
        try:
            if type == 1:
                if request.method == 'POST':
                    # Create the user object
                    user_name = create_user_name(request.form.get("name"))
                    count_user = db.users.find({"user_name": {"$regex": user_name}}).count()
                    user = {
                        "_id": uuid.uuid4().hex,
                        "name": request.form["name"],
                        "user_name": user_name + str(count_user + 1),
                        "email": request.form["email"],
                        "phone": request.form["phone"],
                        "password": request.form.get("password"),
                        "cmnd": request.form.get("cmnd"),
                        "cmnd_1": request.form.get("cmnd_1"),
                        "cmnd_2": request.form.get("cmnd_2"),
                        "note": request.form.get("note"),
                        "is_admin": False
                    }

                    # Encrypt the password
                    user["password"] = generate_password_hash(user["password"])

                    # Check exists email
                    if db.users.find_one({"email": user["email"]}):
                        return jsonify({"error": "Email address already in use"}), 400
                    if db.users.insert_one(user):
                        Logs().insert_log(1, user)
                        return jsonify(user), 200

                return render_template('user/create.html')
            if type == 2:
                return render_template('customer/create.html')
        except Exception as e:
            print(str(e))


    def dashboard(self):
        """
            show dashboard
        :return:
        """
        count_expired = 0
        count_over_expired = 0
        invoices = []
        price_collect = 0
        price_spent = 0
        try:
            today = str(date.today())

            count_expired = len(list(db.invoice.aggregate(eval(g.pipeline_filter_status % (today, today, today, '1')))))
            count_over_expired = len(list(db.invoice.aggregate(eval(g.pipeline_filter_status % (today, today, today, '2')))))
            invoices = list(db.invoice.aggregate(eval(g.pipeline_filter_all % (today, today, today))))

            invoices = [i for i in invoices if not (i['status'] == 0) and not (i['status'] == 10)]  # dashboard : ko lấy hợp đồng đã tất toán

            # print(invoices)
            # invoices['price_pawn'] = ["{:,}".format(float(invoice['price_pawn'])) for invoice in invoices]
            for i in invoices:
                i['price_pawn'] = "{:,.0f}".format(float(i['price_pawn']))
                i['price_rate'] = "{:,.0f}".format(float(i['price_rate']))
                i['from_date'] = dt.datetime.strptime(i['from_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
                i['to_date'] = dt.datetime.strptime(i['to_date'], "%Y-%m-%d").strftime("%d-%m-%Y")


            pipeline_collect = [
                {
                    '$project': {
                        '_id': 0
                    }
                }, {
                    '$match': {
                        'status': 1
                    }
                }, {
                    '$project': {
                        '_id': 0,
                        'collect': 1,
                        'status': 1,
                        'invoice_id': '$collect.source.invoice_id',
                        'note': '$collect.note',
                        'date_created': '$collect.date_created',
                        'user_created': '$collect.user_created',
                        'price': '$collect.price',
                        'type': {
                            '$switch': {
                                'branches': [
                                    {
                                        'case': {
                                            '$eq': [
                                                '$collect.type', 1
                                            ]
                                        },
                                        'then': 'Khác'
                                    }, {
                                        'case': {
                                            '$eq': [
                                                '$collect.type', 2
                                            ]
                                        },
                                        'then': 'Gia hạn'
                                    }, {
                                        'case': {
                                            '$eq': [
                                                '$collect.type', 3
                                            ]
                                        },
                                        'then': 'Tất toán'
                                    }
                                ],
                                'default': '-1'
                            }
                        }
                    }
                },
                {'$sort': {'date_created': -1}}
            ]

            lst_collect = list(db.funds.aggregate(pipeline_collect))
            for i in lst_collect:
                price_collect += int(i["price"])

            pipeline_spent = [
                {
                    '$project': {
                        '_id': 0
                    }
                }, {
                    '$match': {
                        'status': 2
                    }
                }, {
                    '$project': {
                        '_id': 0,
                        'spent': 1,
                        'status': 1,
                        'invoice_id': '$spent.source.invoice_id',
                        'note': '$spent.note',
                        'date_created': '$spent.date_created',
                        'user_created': '$spent.user_created',
                        'price': '$spent.price',
                        'type': {
                            '$switch': {
                                'branches': [
                                    {
                                        'case': {
                                            '$eq': [
                                                '$spent.type', 1
                                            ]
                                        },
                                        'then': 'Khác'
                                    }, {
                                        'case': {
                                            '$eq': [
                                                '$spent.type', 2
                                            ]
                                        },
                                        'then': 'Lập hợp đồng'
                                    }
                                ],
                                'default': '-1'
                            }
                        }
                    }
                },
                {'$sort': {'date_created': -1}}
            ]

            lst_spent = list(db.funds.aggregate(pipeline_spent))
            for i in lst_spent:
                price_spent += int(i["price"])

        except Exception as e:
            print(str(e))
        return render_template('page/dashboard.html', count_expired=count_expired,
                               count_over_expired=count_over_expired,
                               invoices=invoices,
                               price_collect="${:,.0f}".format(float(price_collect)),
                               price_spent="${:,.0f}".format(float(price_spent)))

    def get_invoice(self,id):
        """
            show dashboard
        :return:
        """
        invoice = {}
        try:

            invoice = db.invoice.find_one({"invoice_id":id})
            invoice["from_date"] = dt.datetime.strptime(invoice["from_date"], "%Y-%m-%d").strftime("%d-%m-%Y")
            invoice["to_date"] = dt.datetime.strptime(invoice["to_date"], "%Y-%m-%d").strftime("%d-%m-%Y")
            invoice["date_created"] = dt.datetime.strptime(str(invoice["date_created"]), "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")
            invoice["price_rate"] = "{:,.0f}".format(invoice["price_rate"])
            invoice["price_pawn"] = "{:,.0f}".format(invoice["price_pawn"])

            rate = db.settings.find_one({"kind_item":invoice["item_kind"]})
            # print(invoice)
            if invoice["item_kind"] in ("1", "2", "4", "5", "7", "8", "9"):
                return render_template('page/hopdong.html', invoice=invoice, rate=rate)
            else:
                return render_template('page/hopdong_not.html', invoice=invoice, rate=rate)

        except Exception as e:
            print(str(e))

        return render_template('page/hopdong.html', invoice=invoice, rate=rate)


    def filter(self):
        """
            filter
            :return:
        """
        try:
            users = list(db.users.find({}, {'_id': 0, 'password': 0}))
        except Exception as e:
            print(str(e))
        return render_template('user/list.html', users=users)

    def filter_one(self, email):
        """
            filter one
            :param email:
            :return:
        """
        try:
            user = db.users.find_one({"email": email}, {"_id": 0, "password": 0})
        except Exception as e:
            print(str(e))

        return render_template('user/profile.html', user=user)


class Customer:
    """
        customer class
    """

    def create(self):
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('user/create.html')

    def filter(self):
        try:
            customers = list(db.customers.find({}, {'_id': 0}))
            # print(customers)
        except Exception as e:
            print(str(e))

        return render_template('customer/list.html', customers=customers)

    def filter_one(self, email):
        user = {}
        try:
            user = db.customers.find_one({"email": email}, {"_id": 0})
            # print(user)
        except Exception as e:
            print(str(e))
        return render_template('customer/profile.html', user=user)


class Invoice:
    def create(self):
        """
        - tạo hợp đồng
        funds.collect.type : 1 : THU từ quản lý quỹ / 2 : THU từ tiền lãi  / 3 : THU từ tất toán
        funds.spent.type : 1 : CHI từ quản lý quỹ / 2 : CHI từ làm hợp đồng
        :return:
        """
        try:
            if request.method == 'POST':

                # create treasure object
                invoice_id = request.form.get("pawn_id").replace(" ", "")
                item_kind = request.form.get("pawn_kind_item")
                item_name = request.form.get("pawn_item_name")

                name = request.form.get("pawn_name")
                cmnd = request.form.get("pawn_cmnd")
                from_date = request.form.get("pawn_from_date")
                to_date = request.form.get("pawn_to_date")
                price = request.form.get("pawn_price")

                funds = 0
                treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                if treasure:
                    funds = int(treasure[0]["funds"])
                if db.invoices.find_one({"invoice_id": invoice_id}):
                    error = 'Mã HĐ đã tồn tại'
                    return jsonify({"error": error}), 400
                if name is None or len(name) == 0:
                    error = 'Chưa nhập họ tên KH'
                    return jsonify({"error": error}), 400
                if cmnd is None or len(cmnd) == 0:
                    error = 'Chưa nhập CMND'
                    return jsonify({"error": error}), 400
                if item_kind is None or len(item_kind) == 0:
                    error = 'Chưa chọn loại tài sản'
                    return jsonify({"error": error}), 400
                if item_name is None or len(item_name) == 0:
                    error = 'Chưa nhập tên tài sản'
                    return jsonify({"error": error}), 400
                if price is None or len(price) == 0:
                    error = 'Chưa nhập số tiền vay'
                    return jsonify({"error": error}), 400
                if int(price.replace(',', '')) % 1000 != 0:
                    error = 'Số tiền vay phải chia hết cho 1.000'
                    return jsonify({"error": error}), 400
                if from_date is None or len(from_date) == 0:
                    error = 'Chưa nhập ngày vay'
                    return jsonify({"error": error}), 400
                if to_date is None or len(to_date) == 0:
                    error = 'Chưa nhập ngày đến hạn '
                    return jsonify({"error": error}), 400
                if int(price.replace(',', '')) >= funds:
                    error = 'Quỹ không đủ chi. Cần bổ sung'
                    return jsonify({"error": error}), 400

                days = (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).days
                if days <= 0:
                    error = 'Ngày đến hạn không được nhỏ hơn hoặc bằng ngày vay'
                    return jsonify({"error": error}), 400

                # # check customer . false : create info customer / true : get info customer
                # customer = db.customers.find_one({"cmnd": cmnd})
                # if customer:
                #     pass
                # else:

                # customer
                customer = {
                    "_id": uuid.uuid4().hex,
                    "id": db.customers.find().count() + 1,
                    "name": name,
                    "email": request.form.get("pawn_email"),
                    "phone": request.form.get("pawn_phone"),
                    "cmnd": cmnd,
                    "item_name": item_name,
                    # "cmnd_1": request.form.get("cmnd_1_customer"),
                    # "cmnd_2": request.form.get("cmnd_2_customer"),
                    "address": request.form.get("pawn_address"),
                    "user_created": g.user["user_name"],
                    "date_created": dt.datetime.now()
                }
                db.customers.insert_one(customer)

                Logs().insert_log(2, customer)

                invoice_pawn = {
                    "_id": uuid.uuid4().hex,
                    "invoice_id": invoice_id,
                    "item_kind": item_kind,
                    "item_name": item_name,
                    "customer": customer,
                    "price_pawn": int(price.replace(',', '')),
                    "rate": request.form.get("pawn_rate"),
                    "price_rate": int(request.form.get("pawn_price_rate")),
                    "days": days,
                    "from_date": from_date,
                    "to_date": to_date,
                    "week": int(request.form.get("pawn_week")),
                    "user_created": g.user["user_name"],
                    "date_created": dt.datetime.now(),
                    "status": 1,
                    "note": request.form.get("pawn_note")
                }

                if db.invoice.insert_one(invoice_pawn):

                    Logs().insert_log(3, {"invoice_id": invoice_id, "status": 1, "price": price})  # insert log

                    funds_spent = {
                        "funds": str(funds - int(price.replace(',', ''))),
                        "spent": {
                            "_id": uuid.uuid4().hex,
                            "price": str(price.replace(',', '')),
                            "source": invoice_pawn,
                            "user_created": g.user["user_name"],
                            "date_created": dt.datetime.now(),
                            "note": request.form.get("pawn_note"),
                            "type": 2
                        },
                        "status": 2

                    }
                    db.funds.insert_one(funds_spent)
                return jsonify(invoice_pawn), 200
                # return render_template("report/hopdong_v1.htm")
        except Exception as e:
            print(str(e))
        return render_template('invoice/create.html')

    def pay(self):
        """
        - thanh toán lãi : tính tiền lãi dựa vào số tuần muốn gia hạn
            update from_date = ngày đến hạn thanh toán
                    to_date = from_date + tuần gia hạn
                    status = 2 : trang thái gia hạn
            insert tiền lãi + tiền trả trước (nếu có) vào khoản thu
        funds.collect.type : 1 : THU từ quản lý quỹ / 2 : THU từ tiền lãi
        funds.spent.type : 1 : CHI từ quản lý quỹ / 2 : CHI từ làm hợp đồng
        :return:
        """
        try:
            if request.method == 'POST':
                # create treasure object
                pay_id = request.form.get("pay_id")
                pay_week_ = request.form.get("pay_week_")   # tuần gia hạn
                if pay_week_ is None or len(pay_week_) == 0 or int(pay_week_) < 1:
                    error = 'Nhập số tuần cần gia hạn'
                    return jsonify({"error": error}), 400

                pay_price_ = request.form.get("pay_price_")     # tiền gốc trả trước
                if pay_price_ is None or len(pay_price_) == 0 :
                    pay_price_ = 0
                pay_from_date = request.form.get("pay_to_date")
                pay_from_date_obj = datetime.strptime(pay_from_date, '%d-%m-%Y')    # ngày bắt đầu gia hạn
                pay_to_date = (pay_from_date_obj + timedelta(days=int(pay_week_)*7))  # đến ngày
                # pay_to_date = datetime.strftime(pay_to_date,'%d-%m-%Y')

                # tính lại hợp đồng
                # tiền vay = tiền đã vay - tiền trả trước (nếu có)
                price_pawn = int(request.form.get("pay_price").replace(',', '')) - int(str(pay_price_).replace(',', ''))
                # tiền lãi = (tiền lãi đã tính / tuần ) * tuần vay mới
                price_rate = int(request.form.get("pay_price_rate").replace(',', ''))/int(request.form.get("pay_week"))*int(pay_week_)
                # khoản thu thực tế
                price_collect = int(str(pay_price_).replace(',', '')) + int(request.form.get("pay_price_rate").replace(',', ''))

                # update hợp đồng + insert khoản thu
                funds = 0
                if db.invoice.update_one({"invoice_id":pay_id},
                                                {
                                                    "$set":{"week":pay_week_,
                                                            "from_date": datetime.strftime(pay_from_date_obj,'%Y-%m-%d'),
                                                            "to_date": datetime.strftime(pay_to_date,'%Y-%m-%d'),
                                                            "price_pawn": price_pawn,
                                                            "price_rate": price_rate,
                                                            "user_modify": g.user["user_name"],
                                                            "date_modify": dt.datetime.now(),
                                                            "days": (int(pay_week_)*7),
                                                            "status": 2
                                                            }}):
                    Logs().insert_log(3, {"invoice_id": pay_id, "status": 2, "price": str(funds + price_collect).replace(',', '')})
                    treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                    if treasure:
                        funds = int(treasure[0]["funds"])
                    funds_collect = {
                        "funds": str(funds + price_collect),   # + tiền lãi + tiền gốc trả trước (nếu có)
                        "collect": {
                            "_id": uuid.uuid4().hex,
                            "price": str(price_collect),
                            "source": db.invoice.find_one({"invoice_id": pay_id},{"_id": 0}),
                            "user_created": g.user["user_name"],
                            "date_created": dt.datetime.now(),
                            "note": request.form.get("pay_note"),
                            "type": 2,  # 2. khoản thu từ lãi của hợp đồng
                        },
                        "status": 1
                    }
                    db.funds.insert_one(funds_collect)


                return jsonify(), 200
        except Exception as e:
            print(str(e))
        return render_template('invoice/pay.html')

    def pay_id(self, id):
        """
        - thanh toán lãi : tính tiền lãi dựa vào số tuần muốn gia hạn
            update from_date = ngày đến hạn thanh toán
                    to_date = from_date + tuần gia hạn
                    status = 2 : trang thái gia hạn
            insert tiền lãi + tiền trả trước (nếu có) vào khoản thu
        funds.collect.type : 1 : THU từ quản lý quỹ / 2 : THU từ tiền lãi
        funds.spent.type : 1 : CHI từ quản lý quỹ / 2 : CHI từ làm hợp đồng
        :return:
        """
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('invoice/pay.html')

    def redeem(self):
        """
        - tất toán : tính tiền lãi + tiền gốc
            update invoice.status = 0
            insert tiền lãi + tiền gốc vào khoản thu
        funds.collect.type : 1 : THU từ quản lý quỹ / 2 : THU từ tiền lãi
        funds.spent.type : 1 : CHI từ quản lý quỹ / 2 : CHI từ làm hợp đồng
        :return:
        """
        try:
            if request.method == 'POST':
                # create treasure object
                redeem_id = request.form.get("redeem_id")

                redeem_price = int(request.form.get("redeem_price").replace(',', ''))  # tiền gốc / số tiền vay

                redeem_price_rate = int(request.form.get("redeem_price_rate").replace(',', '')) # tiền lãi
                redeem_price_rate_real = request.form.get("redeem_price_rate_real").replace(',', '')  # tiền lãi thực tế
                # print(redeem_price_rate_real)
                if redeem_price_rate_real != '' and len(redeem_price_rate_real) > 0:
                    redeem_price_rate = int(redeem_price_rate_real) # hợp đồng tất toán sớm

                # update hợp đồng + insert khoản thu
                funds = 0
                print(str(funds + redeem_price + redeem_price_rate))
                if db.invoice.update_one({"invoice_id": redeem_id},{"$set": {"status": 0}}):
                    Logs().insert_log(3, {"invoice_id": redeem_id, "status": 0, "price": str(redeem_price + redeem_price_rate).replace(',', '')})
                    treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                    if treasure:
                        funds = int(treasure[0]["funds"])
                    funds_collect = {
                        "funds": str(funds + redeem_price + redeem_price_rate),  # + tiền lãi + tiền gốc
                        "collect": {
                            "_id": uuid.uuid4().hex,
                            "price": str(redeem_price + redeem_price_rate),
                            "source": db.invoice.find_one({"invoice_id": redeem_id},{"_id": 0}),
                            "user_created": g.user["user_name"],
                            "date_created": dt.datetime.now(),
                            "note": request.form.get("redeem_note"),
                            "type": 3,  # 3. khoản thu từ tất toán hợp đồng
                        },
                        "status": 1

                    }
                    db.funds.insert_one(funds_collect)

                return jsonify(), 200
        except Exception as e:
            print(str(e))
        return render_template('invoice/redeem.html')

    def redeem_id(self, id):
        """
        :return:
        """
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('invoice/redeem.html')

    def filter(self):
        invoices = []
        total = 0
        total_rate = 0
        try:
            today = str(date.today())
            invoices = list(db.invoice.aggregate(eval(g.pipeline_filter_all % (today, today, today))))
            for i in invoices:
                total += i['price_pawn']
                total_rate += i['price_rate']
                i['price_pawn'] = "{:,.0f}".format(float(i['price_pawn']))
                i['price_rate'] = "{:,.0f}".format(float(i['price_rate']))
                i['from_date'] = dt.datetime.strptime(i['from_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
                i['to_date'] = dt.datetime.strptime(i['to_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            total = "{:,.0f}".format(float(total))
            total_rate= "{:,.0f}".format(float(total_rate))
            # print(invoices)
        except Exception as e:
            print(str(e))
        return render_template('invoice/list.html', invoices=invoices, total=total, total_rate=total_rate)

    def filter_expired(self):
        """
         filter hợp đồng đến hạn : status in (1,2) và to_date = today()
        :return:
        """
        invoices = []
        try:

            today = str(date.today())
            invoices = list(db.invoice.aggregate(eval(g.pipeline_filter_status % (today, today, today, '1'))))
            for i in invoices:
                i['price_pawn'] = "{:,.0f}".format(float(i['price_pawn']))
                i['price_rate'] = "{:,.0f}".format(float(i['price_rate']))
                i['from_date'] = dt.datetime.strptime(i['from_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
                i['to_date'] = dt.datetime.strptime(i['to_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except Exception as e:
            print(str(e))
        return render_template('invoice/list.html', invoices=invoices, count_invoice=len(invoices))

    def filter_over_expired(self):
        """
            filter hợp đồng quá hạn : status in (1,2) và to_date > today()
        :return:
        """
        invoices = []
        try:
            today = str(date.today())
            invoices = list(db.invoice.aggregate(eval(g.pipeline_filter_status % (today, today, today, '2'))))
            for i in invoices:
                i['price_pawn'] = "{:,.0f}".format(float(i['price_pawn']))
                i['price_rate'] = "{:,.0f}".format(float(i['price_rate']))
                i['from_date'] = dt.datetime.strptime(i['from_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
                i['to_date'] = dt.datetime.strptime(i['to_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except Exception as e:
            print(str(e))
        return render_template('invoice/list.html', invoices=invoices, count_invoice=len(invoices))

    def filter_one(self,id):
        try:
            invoices = db.invoice.find_one( {"$or":[{"status":1},{"status":2}],"invoice_id":id} )
            invoices['price_pawn'] = "{:,.0f}".format(float(invoices['price_pawn']))
            invoices['price_rate'] = "{:,.0f}".format(float(invoices['price_rate']))
            # print(invoices['from_date'])
            invoices['from_date'] = dt.datetime.strptime(invoices['from_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            invoices['to_date'] = dt.datetime.strptime(invoices['to_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        except Exception as e:
            print(str(e))
        return jsonify(invoices), 200


class Settings:
    def get_rate_kind_item(self, kind_item):
        rate = 0
        try:
            setting = db.settings.find_one({"kind_item": str(kind_item), "status": "1"}, {"_id": 0})
            if setting:
                rate = int(setting["rate"]) + int(setting["service_charge"]) + int(setting["storage_charge"])
        except Exception as e:
            print(str(e))
        return jsonify(setting), 200

    def set_rate(self, kind_item):
        setting = {}
        try:
            setting = db.settings.find_one({"kind_item": str(kind_item), "status": "1"},{"_id": 0})
            # print(setting)
        except Exception as e:
            print(str(e))
        return jsonify(setting), 200

    def update_rate(self):
        try:
            if request.method == "POST":
                upd_kind_item = str(request.form.get("upd_kind_item"))
                upd_item_name = request.form.get("upd_item_name")
                upd_rate = str(request.form.get("upd_rate"))
                upd_service_charge = str(request.form.get("upd_service_charge"))
                upd_storage_charge = str(request.form.get("upd_storage_charge"))
                if db.settings.find_one({"kind_item": upd_kind_item, "status": "1"}):
                    db.settings.update_one({"kind_item": upd_kind_item, "status": "1"},
                                       {"$set":
                                            {"item_name": upd_item_name,
                                             "rate": upd_rate,
                                             "service_charge": upd_service_charge,
                                             "storage_charge": upd_storage_charge}})

                else:
                    db.settings.insert_one({
                                                 "kind_item": upd_kind_item,
                                                 "item_name": upd_item_name,
                                                 "rate": upd_rate,
                                                 "service_charge": upd_service_charge,
                                                 "storage_charge": upd_storage_charge,
                                                 "status": "1"})
                Logs().insert_log(4, {
                    "kind_item": upd_kind_item,
                    "item_name": upd_item_name,
                    "rate": upd_rate,
                    "service_charge": upd_service_charge,
                    "storage_charge": upd_storage_charge
                })
                return jsonify({"result": "1", "msg": "update done"}), 200
        except Exception as e:
            print(str(e))
        return render_template('settings/set_rate.html')

    def set_rules(self):
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('settings/set_rule.html')

    def filter_rate(self):
        try:
            lst_rate = db.settings.find({"status": "1"}, {"_id": 0})
        except Exception as e:
            print(str(e))
        return render_template('settings/list_rate.html', lst_rate=lst_rate)


class Funds:
    def collect(self):
        """
            nạp vào
            funds.status = 1
        :return:
        """
        try:
            if request.method == "POST":
                price = request.form.get("price")
                if price is None or len(price) == 0:
                    error = 'Số tiền chưa nhập'
                    return jsonify({"error": error}), 400
                price = int(price.replace(',', ''))
                if price % 1000 !=0:
                    error = 'Số tiền phải chia hết cho 10.000'
                    return jsonify({"error": error}), 400
                source = {"invoice_id": "","source": request.form.get("source")}
                user_created = request.form.get("user_created")
                note = request.form.get("note")
                funds = 0
                treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                if treasure:
                    funds = int(treasure[0]["funds"])

                funds_collect = {
                    "funds": str(funds + price),
                    "collect": {
                        "_id": uuid.uuid4().hex,
                        "price": str(price),
                        "source": source,
                        "user_created": g.user["user_name"],
                        "date_created": dt.datetime.now(),
                        "note": note,
                        "type": 1
                    },
                    "status": 1

                }
                db.funds.insert_one(funds_collect)
                Logs().insert_log(5, funds_collect)
                return jsonify(), 200
        except Exception as e:
            print(str(e))

        return render_template('funds/collect.html')

    def spent(self):
        """
                    chi ra
                    funds.status = 2
                :return:
                """
        error = None
        try:
            if request.method == "POST":
                price = request.form.get("price")
                if price is None or len(price) == 0:
                    error = 'Số tiền chưa nhập'
                    return jsonify({"error": error}), 400
                price = int(price.replace(',', ''))
                if price % 1000 !=0:
                    error = 'Số tiền phải chia hết cho 10.000'
                    return jsonify({"error": error}), 400
                source = {"invoice_id": "","source": request.form.get("source")}
                user_created = request.form.get("user_created")
                note = request.form.get("note")

                treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                if treasure:
                    funds = int(treasure[0]["funds"])
                funds_spent = {
                    "funds": str(funds - price),
                    "spent": {
                        "_id": uuid.uuid4().hex,
                        "price": str(price),
                        "source": source,
                        "user_created": g.user["user_name"],
                        "date_created": dt.datetime.now(),
                        "note": note,
                        "type": 1
                    },
                    "status": 2
                }
                db.funds.insert_one(funds_spent)
                Logs().insert_log(6, funds_spent)
                return jsonify(), 200
        except Exception as e:
            print(str(e))

        return render_template('funds/spent.html')
    def filter(self):
        lst_collect = []
        price_collect = 0
        price_collect_invoice = 0
        price_collect_other = 0
        lst_spent = []
        price_spent = 0
        price_spent_invoice = 0
        price_spent_other = 0
        try:
            pipeline_collect = [
                            {
                                '$project': {
                                    '_id': 0
                                }
                            }, {
                                '$match': {
                                    'status': 1
                                }
                            }, {
                                '$project': {
                                    '_id': 0,
                                    'collect': 1,
                                    'status': 1,
                                    'invoice_id': '$collect.source.invoice_id',
                                    'item_name': '$collect.source.item_name',
                                    'note': '$collect.note',
                                    'date_created': '$collect.date_created',
                                    'user_created': '$collect.user_created',
                                    'price': '$collect.price',
                                    'type': {
                                        '$switch': {
                                            'branches': [
                                                {
                                                    'case': {
                                                        '$eq': [
                                                            '$collect.type', 1
                                                        ]
                                                    },
                                                    'then': 'Khác'
                                                }, {
                                                    'case': {
                                                        '$eq': [
                                                            '$collect.type', 2
                                                        ]
                                                    },
                                                    'then': 'Gia hạn'
                                                }, {
                                                    'case': {
                                                        '$eq': [
                                                            '$collect.type', 3
                                                        ]
                                                    },
                                                    'then': 'Tất toán'
                                                }
                                            ],
                                            'default': '-1'
                                        }
                                    }
                                }
                            },
                            {'$sort':{'date_created':-1}}
                        ]

            lst_collect = list(db.funds.aggregate(pipeline_collect))
            for i in lst_collect:
                price_collect += int(i["price"])
                if i["type"] == "Khác":
                    price_collect_other += int(i["price"])
                else:
                    price_collect_invoice += int(i["price"])
                i["price"] = "{:,.0f}".format(float(i["price"]))
                i["date_created"] = dt.datetime.strptime(str(i["date_created"]), "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M")

            pipeline_spent = [
                {
                    '$project': {
                        '_id': 0
                    }
                }, {
                    '$match': {
                        'status': 2
                    }
                }, {
                    '$project': {
                        '_id': 0,
                        'spent': 1,
                        'status': 1,
                        'invoice_id': '$spent.source.invoice_id',
                        'item_name': '$spent.source.item_name',
                        'note': '$spent.note',
                        'date_created': '$spent.date_created',
                        'user_created': '$spent.user_created',
                        'price': '$spent.price',
                        'type': {
                            '$switch': {
                                'branches': [
                                    {
                                        'case': {
                                            '$eq': [
                                                '$spent.type', 1
                                            ]
                                        },
                                        'then': 'Khác'
                                    }, {
                                        'case': {
                                            '$eq': [
                                                '$spent.type', 2
                                            ]
                                        },
                                        'then': 'Lập hợp đồng'
                                    }
                                ],
                                'default': '-1'
                            }
                        }
                    }
                },
                {'$sort': {'date_created': -1}}
            ]

            lst_spent = list(db.funds.aggregate(pipeline_spent))
            for i in lst_spent:
                price_spent += int(i["price"])
                if i["type"] == "Khác":
                    price_spent_other += int(i["price"])
                else:
                    price_spent_invoice += int(i["price"])
                i["price"] = "{:,.0f}".format(float(i["price"]))
                i["date_created"] = dt.datetime.strptime(str(i["date_created"]), "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y %H:%M")
            # print(price_collect)
            # print(price_spent)
        except Exception as e:
            print(str(e))
        return render_template('funds/list.html', lst_collect=lst_collect,
                                                    price_collect = "${:,.0f}".format(float(price_collect)),
                                                    price_collect_invoice="${:,.0f}".format(float(price_collect_invoice)),
                                                    price_collect_other="${:,.0f}".format(float(price_collect_other)),
                                                    lst_spent=lst_spent,
                                                    price_spent = "${:,.0f}".format(float(price_spent)),
                                                    price_spent_invoice = "${:,.0f}".format(float(price_spent_invoice)),
                                                    price_spent_other = "${:,.0f}".format(float(price_spent_other)))


class Logs:
    def insert_log(self, type, dict):
        """
        type = 1 : log user
                2 : log customer
                3 : log invoice
                4 : log settings
                5 : log funds
        :param type:
        :param dict:
        :return:
        """
        try:

            log_dict = {
                "user_created": g.user["user_name"],
                "date_created": dt.datetime.now(),
                "log": ""
            }
            if type == 1:   # log user
                log_dict["log"] = dict["user_name"] + " đã được tạo "
            if type == 2:   # log customer
                log_dict["log"] = dict["name"] + " là khách hàng mới "
            if type == 3:   # log invoice
                if dict["status"] == 1: # hợp đồng mới
                    log_dict["log"] = "Chi " + dict["price"] + " - Note : lập hợp đồng " + dict["invoice_id"]
                if dict["status"] == 2: # hợp đồng trả lãi
                    log_dict["log"] = "Thu " + "{:,.0f}".format(float(dict["price"])) + " - Note :  thu lãi hợp đồng " + dict["invoice_id"]
                if dict["status"] == 0: # hợp đồng tất toán
                    log_dict["log"] = "Thu " + "{:,.0f}".format(float(dict["price"])) + " - Note :  tất toán hợp đồng " + dict["invoice_id"]
            if type == 4:   # log settings
                log_dict["log"] = "Cập nhật lãi suất cho " + dict["item_name"]
            if type == 5:   # log funds.collect
                if dict["collect"]:
                    log_dict["log"] = dict["collect"]["source"]['source'] + " Nạp vào " + "{:,.0f}".format(float(dict["collect"]["price"])) + " - Note : " + dict["collect"]["note"]
            if type == 6:   # log funds.spent
                if dict["spent"]:
                    log_dict["log"] = dict['spent']["source"]["source"] + " Chi ra " + "{:,.0f}".format(float(dict["spent"]["price"])) + " - Note : " + dict["spent"]["note"]

            db.logs.insert_one(log_dict)
        except Exception as e:
            print(str(e))


