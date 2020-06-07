from flask_login import UserMixin
import _sqlite3 as sql

class User(UserMixin):

    def __init__(self, id, name, username, password, email):
        self.id = id
        self.name = name
        self.username = username.lower()
        self.password = password
        self.email = email
        self.admin = 0

    def is_authenticated():
        return True

    def is_active():
        return True

    def is_annonymous():
        return False

    def get_id(self):
        con = sql.connect('database.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select id from users where username = ?', (self.username,))
        id = cur.fetchone()
        return id[0]

    def get_username(self):
        return self.username

    def add_db(self):
        curs = g.db.cursor()
        curs.execute('insert into user(username, password, email) values (?, ?, ?)',
                     [self.username, self.password, self.email])
        g.db.commit()

    def is_admin(self):
        con = sql.connect('database.db')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute('select is_admin from users where username = ?', (self.username,))
        is_admin = cur.fetchone()
        self.is_admin = int(is_admin[0])
        return self.is_admin
