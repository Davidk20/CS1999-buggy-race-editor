from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, Blueprint
from flask_login import LoginManager
import sqlite3 as sql
from .form_validation import buggy_validation
from .cost_method import cost_method


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisthesecretkey'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .user_model import User

    @login_manager.user_loader
    def load_user(id):
        con = sql.connect('database.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE id =?',(id,))
        user = cur.fetchone()
        if user is not None:
            return User(user[0], user[1], user[2],user[3],user[4])
        else:
            return 'User not found.'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == '__main__':
    create_app()
