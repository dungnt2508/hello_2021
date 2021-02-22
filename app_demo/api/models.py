from flask import Flask, jsonify, request, session, redirect, render_template, url_for, flash, g
from passlib.hash import pbkdf2_sha256
import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from app_demo.db import db


class User:

    def load_logged_in_user(self):
        user_id = session.get('id')

        if user_id is None:
            g.user = None
        else:
            g.user = db.users.find_one({"_id": user_id})
        # print(g.auth)

    def register(self):
        if request.method == 'POST':
            # Create the auth object
            user = {
                "_id": uuid.uuid4().hex,
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "password": request.form.get("password")
            }

            # Encrypt the password
            user["password"] = generate_password_hash(user["password"])

            # Check exists email
            if db.users.find_one({"email": user["email"]}):
                return jsonify({"error": "Email address already in use"}), 400
            if db.users.insert_one(user):
                session.clear()
                session['name'] = user['name']
                session['id'] = str(user['_id'])
                return jsonify(user), 200

        return render_template('auth/register.html')

    def login(self):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            error = None
            user = db.users.find_one({'email': email})

            if user is None:
                error = 'Incorrect username.'
                return jsonify({"error": error}), 400
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
                return jsonify({"error": error}), 400

            if error is None:
                session.clear()
                session['email'] = user['email']
                session['id'] = str(user['_id'])
                # print(session)

                return jsonify(user), 200

            flash(error)

        return render_template('auth/login.html')

    def logout(self):
        session.clear()
        return redirect("/")

    def dashboard(self):
        return render_template('page/dashboard.html')