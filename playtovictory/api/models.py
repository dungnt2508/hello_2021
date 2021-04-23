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
                    g.customers = list(db.customers.aggregate([{"$sort": {"_id": 1}}]))[0]

                # get quĩ
                g.treasure = 0
                if db.funds.find_one():
                    g.treasure = "${:,.0f}".format(float(list(db.funds.aggregate([{"$sort": {"_id": -1}}, {"$limit": 1}]))[0]["funds"]))
                # print(g.settings)
                today = datetime.combine(date.today(), datetime.min.time())
                g.logs = list(db.logs.find({"date_created": {"$gte": today}}))
                # print(g.logs)
                # setting filter
                g.pipeline_filter_status = "[ { '$project': { '_id': 0, 'invoice_id': 1, 'item_kind': 1, 'item_name': 1, 'customer': 1, 'price_pawn': 1, 'rate': 1, 'price_rate': 1, 'from_date': 1, 'to_date': 1, 'user_created': 1, 'date_created': 1, 'status': 1, 'status_invoice': { '$switch': { 'branches': [ { 'case': { '$and': [ { '$gt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '0' }, { 'case': { '$and': [ { '$eq': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '1' }, { 'case': { '$and': [ { '$lt': [ '$to_date', '%s' ] }, { '$in': [ '$status', [ 1, 2 ] ] } ] }, 'then': '2' },{ 'case': { '$and': [ { '$eq': [ '1', '1' ] }, { '$in': [ '$status', [ 10, 10 ] ] } ] }, 'then': '10' } ], 'default': '-1' } } } },{ '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1,'status_invoice':1, 'status_invoice_msg':{ '$switch':{ 'branches':[ { 'case':{ '$eq':[ '$status_invoice', '0' ] }, 'then':'Bình thường' }, { 'case':{ '$eq':[ '$status_invoice', '1' ] }, 'then':'Đến hạn' }, { 'case':{ '$eq':[ '$status_invoice', '2' ] }, 'then':'Quá hạn' },{ 'case':{ '$eq':[ '$status_invoice', '10' ] }, 'then':'Đã xóa' } ], 'default':'Đã tất toán' } } } }, { '$match': { 'status_invoice': '%s' } },{ '$lookup': {'from': 'settings', 'localField': 'item_kind', 'foreignField': 'kind_item', 'as': 'rate_invoice' }} ]"
                g.pipeline_filter_all = "[ { '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1, 'status_invoice':{ '$switch':{ 'branches':[ { 'case':{ '$and':[ { '$gt':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'0' }, { 'case':{ '$and':[ { '$eq':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'1' }, { 'case':{ '$and':[ { '$lt':[ '$to_date', '%s' ] }, { '$in':[ '$status', [ 1, 2 ] ] } ] }, 'then':'2' },{ 'case': { '$and': [ { '$eq': [ '1', '1' ] }, { '$in': [ '$status', [ 10, 10 ] ] } ] }, 'then': '10' } ], 'default':'-1' } } } }, { '$project':{ '_id':0, 'invoice_id':1, 'item_kind':1, 'item_name':1, 'customer':1, 'price_pawn':1, 'rate':1, 'price_rate':1, 'from_date':1, 'to_date':1, 'user_created':1, 'date_created':1, 'status':1, 'status_invoice_msg':{ '$switch':{ 'branches':[ { 'case':{ '$eq':[ '$status_invoice', '0' ] }, 'then':'Bình thường' }, { 'case':{ '$eq':[ '$status_invoice', '1' ] }, 'then':'Đến hạn' }, { 'case':{ '$eq':[ '$status_invoice', '2' ] }, 'then':'Quá hạn' },{ 'case':{ '$eq':[ '$status_invoice', '10' ] }, 'then':'Đã xóa' } ], 'default':'Đã tất toán' } } } },{ '$lookup': {'from': 'settings', 'localField': 'item_kind', 'foreignField': 'kind_item', 'as': 'rate_invoice' }} ]"

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
                    # Logs().insert_log(1, user)
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
                {'$sort': {'_id': 1}}
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
                {'$sort': {'_id': 1}}
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
