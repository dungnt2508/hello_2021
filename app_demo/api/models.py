from flask import Flask, jsonify, request, session, redirect, render_template, url_for, flash, g
from passlib.hash import pbkdf2_sha256
import uuid
import datetime as dt
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app_demo.db import db
from instance.rule_name import create_user_name

import pandas as pd


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


                # if db.settings.find({"status": 1}, {"_id": 0}).count() == 0:
                #     db.settings.insert_many([{
                #         "kind_item": "1",
                #         "item_name": "Cầm giấy tờ",
                #         "rate": "1",
                #         "service_charge": "7",
                #         "storage_charge": "7",
                #         "status": "1"
                #     }, {
                #         "kind_item": "2",
                #         "item_name": "Cầm xe máy chính chủ",
                #         "rate": "1",
                #         "service_charge": "1",
                #         "storage_charge": "4",
                #         "status": "1"
                #     }, {
                #         "kind_item": "3",
                #         "item_name": "Cầm xe máy không chính chủ",
                #         "rate": "1",
                #         "service_charge": "10",
                #         "storage_charge": "4",
                #         "status": "1"
                #     }, {
                #         "kind_item": "4",
                #         "item_name": "Cầm điện thoại, Ipad, Laptop",
                #         "rate": "1",
                #         "service_charge": "7",
                #         "storage_charge": "4",
                #         "status": "1"
                #     }, {
                #         "kind_item": "5",
                #         "item_name": "Cầm oto chính chủ",
                #         "rate": "1",
                #         "service_charge": "1",
                #         "storage_charge": '4',
                #         "status": "1"
                #     }, {
                #         "kind_item": "6",
                #         "item_name": "Cầm oto không chính chủ",
                #         "rate": "1",
                #         "service_charge": "7",
                #         "storage_charge": "7",
                #         "status": "1"
                #     }, {
                #         "kind_item": "7",
                #         "item_name": "Cầm oto ngân hàng chính chủ",
                #         "rate": "1",
                #         "service_charge": "5",
                #         "storage_charge": "4",
                #         "status": "1"
                #     }, {
                #         "kind_item": "8",
                #         "item_name": "Cầm nhà đất",
                #         "rate": "1",
                #         "service_charge": "3",
                #         "storage_charge": "0",
                #         "status": "1"
                #     }, {
                #         "kind_item": "9",
                #         "item_name": "Cầm nhà đất ngân hàng",
                #         "rate": "1",
                #         "service_charge": "3",
                #         "storage_charge": "0",
                #         "status": "1"
                #     }])
                g.settings = db.settings.find({"status": "1"}, {"_id": 0})
                g.total_invoice = 0
                if db.invoice.find(({"status": 1})).count() > 0:
                    g.total_invoice = db.invoice.find(({"status": 1})).count()
                g.total_customer = db.customers.find().count()
                g.customer = []
                if g.total_customer != 0:
                    g.customers = list(db.customers.aggregate([{"$sort": {"_id": 1}}]))[0]

                # get quĩ
                g.treasure = 0
                if db.funds.find_one():
                    g.treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))[0]["funds"]
                # print(g.settings)

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
            pass
        except Exception as e:
            print(str(e))
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

        return render_template('user/login.html')

    def logout(self):
        """
            logout
        :return:
        """
        try:
            pass
        except Exception as e:
            print(str(e))
        session.clear()
        return redirect("/")

    def create(self, type):
        """
            create
            :param type:
            :return:
        """
        try:
            pass
        except Exception as e:
            print(str(e))
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
                    return jsonify(user), 200

            return render_template('user/create.html')
        if type == 2:
            return render_template('customer/create.html')

    def dashboard(self):
        """
            show dashboard
        :return:
        """
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('page/dashboard.html')

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
        # if type == 1:
        #     if request.method == 'POST':
        #         # Create the user object
        #         user_name = create_user_name(request.form.get("name"))
        #         count_user = db.users.find({"user_name": {"$regex": user_name}}).count()
        #         user = {
        #             "_id": uuid.uuid4().hex,
        #             "name": request.form.get("name"),
        #             "user_name": user_name + str(count_user + 1),
        #             "email": request.form.get("email"),
        #             "phone": request.form.get("phone"),
        #             "password": request.form.get("password"),
        #             "cmnd_1": request.form.get("cmnd_1"),
        #             "cmnd_2": request.form.get("cmnd_2"),
        #             "note": request.form.get("note"),
        #             "is_admin": False
        #         }
        #
        #         # Encrypt the password
        #         user["password"] = generate_password_hash(user["password"])
        #
        #         # Check exists email
        #         if db.users.find_one({"email": user["email"]}):
        #             return jsonify({"error": "Email address already in use"}), 400
        #         if db.users.insert_one(user):
        #             session.clear()
        #             session['name'] = user['name']
        #             session['user_name'] = user['user_name']
        #             session['id'] = str(user['_id'])
        #             return jsonify(user), 200
        #
        #     return render_template('user/create.html')
        # if type == 2:
        #     return render_template('user/create.html')
        return render_template('user/create.html')

    def filter(self):
        try:
            customers = list(db.customers.find({}, {'_id': 0}))
            # print(customers)
        except Exception as e:
            print(str(e))

        return render_template('customer/list.html', customers=customers)

    def filter_one(self, email):
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
        funds.collect.type : 1 : THU từ quản lý quỹ / 2 : THU từ tiền lãi
        funds.spent.type : 2 : CHI từ quản lý quỹ / 2 : CHI từ làm hợp đồng
        :return:
        """
        try:
            if request.method == 'POST':

                # create treasure object
                invoice_id = request.form.get("invoice_id")
                item_kind = request.form.get("kind_item")
                item_name = request.form.get("item_name")

                name = request.form.get("name")
                cmnd = request.form.get("cmnd")
                from_date = request.form.get("from_date")
                to_date = request.form.get("to_date")
                price = request.form.get("price")

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
                if from_date is None or len(from_date) == 0:
                    error = 'Chưa nhập ngày vay'
                    return jsonify({"error": error}), 400
                if to_date is None or len(to_date) == 0:
                    error = 'Chưa nhập ngày đến hạn '
                    return jsonify({"error": error}), 400

                days = (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).days
                if days <= 0:
                    error = 'Ngày đến hạn không được nhỏ hơn hoặc bằng ngày vay'
                    return jsonify({"error": error}), 400

                # check customer . false : create info customer / true : get info customer
                customer = db.customers.find_one({"cmnd": cmnd})
                if customer:
                    pass
                else:

                    # customer
                    customer = {
                        "_id": uuid.uuid4().hex,
                        "id": db.customers.find().count() + 1,
                        "name": name,
                        "email": request.form.get("email"),
                        "phone": request.form.get("phone"),
                        "cmnd": cmnd,
                        "item_name": item_name,
                        # "cmnd_1": request.form.get("cmnd_1_customer"),
                        # "cmnd_2": request.form.get("cmnd_2_customer"),
                        "address": request.form.get("address"),
                        "user_created": g.user["user_name"],
                        "date_created": dt.datetime.now()
                    }
                    db.customers.insert_one(customer)

                invoice_pawn = {
                    "_id": uuid.uuid4().hex,
                    "invoice_id": invoice_id,
                    "item_kind": item_kind,
                    "item_name": item_name,
                    "customer": customer,
                    "price_pawn": price,
                    "rate": request.form.get("rate"),
                    "price_rate": request.form.get("price_rate"),
                    "days": days,
                    "from_date": from_date,
                    "to_date": to_date,
                    "user_created": g.user["user_name"],
                    "date_created": dt.datetime.now(),
                    "type": 1,  # 1 : lập hợp đồng vay
                    "status": 1,
                    "note": request.form.get("note")
                }
                funds = 0
                if db.invoice.insert_one(invoice_pawn):
                    treasure = list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))
                    if treasure:
                        funds = int(treasure[0]["funds"])
                    funds_spent = {
                        "funds": str(funds - int(price)),
                        "spent": {
                            "_id": uuid.uuid4().hex,
                            "price": str(price),
                            "source": invoice_pawn,
                            "user_created": g.user["user_name"],
                            "note": request.form.get("note"),
                            "type": 2,
                            "status": 1
                        }

                    }
                    db.funds.insert_one(funds_spent)
                return jsonify(invoice_pawn), 200
        except Exception as e:
            print(str(e))
        return render_template('invoice/create.html')

    def filter(self):
        try:
            invoices = list(db.invoice.find({}, {'_id': 0}))
            # print(invoices)
        except Exception as e:
            print(str(e))
        return render_template('user/list.html', invoices=invoices)


class Settings:
    def get_rate(self, kind_item):
        try:
            rate = 0
            setting = db.settings.find_one({"kind_item": str(kind_item), "status": "1"}, {"_id": 0})
            if setting:
                rate = int(setting["rate"]) + int(setting["service_charge"]) + int(setting["storage_charge"])
        except Exception as e:
            print(str(e))
        return jsonify(rate), 200

    def set_rules(self):
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('settings/set_rule.html')

    def set_rate(self):
        try:
            pass
        except Exception as e:
            print(str(e))
        return render_template('settings/set_rate.html')


class Funds:
    def collect(self):
        try:
            if request.method == "POST":
                price = int(request.form.get("price"))
                source = request.form.get("source")
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
                        "user_created": user_created,
                        "date_created": dt.datetime.now(),
                        "note": note,
                        "type": 1,
                        "status": 1
                    }

                }
                db.funds.insert_one(funds_collect)
                return jsonify(), 200
        except Exception as e:
            print(str(e))

        return render_template('funds/collect.html')

    def spent(self):
        try:
            if request.method == "POST":
                price = int(request.form.get("price"))
                source = request.form.get("source")
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
                        "user_created": user_created,
                        "date_created": dt.datetime.now(),
                        "note": note,
                        "type": 1,
                        "status": 1
                    }

                }
                db.funds.insert_one(funds_spent)
                return jsonify(), 200
        except Exception as e:
            print(str(e))

        return render_template('funds/spent.html')