from flask import Flask, render_template, request, jsonify, flash, Blueprint, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
auth = Blueprint('auth',__name__)
DATABASE_FILE = "database.db"




@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        username = username.lower()
        password = request.form.get('password')
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?",(username,))
        user = cur.fetchone()
        if not user or not check_password_hash(user[3],password):
                flash('Incorrect Username / Password please try again')
                return redirect(url_for('auth.login'))
        else:
            from .user_model import User as userData
            user = userData(user[0],user[1],user[2],user[3],user[4])
            login_user(user)
            if password == 'Pass1234':
                print('yeet')
                flash('Your password has been reset, please change before continuing')
                return redirect(url_for('main.home'))
                #TODO change this to personal UAC when created
            return redirect(url_for('main.home'))

@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        conf_pass = request.form.get('confirmed_password', False)
        if password != conf_pass:
            flash('Passwords do not match', 'warning')
            return render_template('signup.html')
        else:
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            accounts = cur.fetchall()
            for user in range(len(accounts)):
                if username == accounts[user][2]:
                    flash('Account name already in use', 'warning')
                    return render_template('signup.html')
                elif email == accounts[user][4]:
                    flash('Account already exists', 'warning')
                    return render_template('login.html')
            password = generate_password_hash(password)
            try:
                con = sql.connect(DATABASE_FILE)
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute("INSERT INTO users (name, username, password, email) VALUES(?,?,?,?)",(name,username,password,email))
                con.commit()
            except:
                flash('Error in account creation', 'warning')
            finally:
                con.close()
                return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'warning')
    return redirect(url_for('main.home'))

