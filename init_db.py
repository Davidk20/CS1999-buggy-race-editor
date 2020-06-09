import sqlite3, csv
from werkzeug.security import generate_password_hash
DATABASE_FILE = "database.db"
CSV_FILE = "buggy_costs.csv"
# important:
#-------------------------------------------------------------
# This script initialises your database for you using SQLite,
#-------------------------------------------------------------
con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))
cur = con.cursor()


con.execute("""
    CREATE TABLE IF NOT EXISTS buggies (
        id	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        qty_wheels	INTEGER,
        power_type	TEXT,
        power_units	INTEGER,
        aux_power_type	TEXT,
        aux_power_units	INTEGER,
        hamster_booster	INTEGER,
        flag_color_primary	VARCHAR(20),
        flag_color_secondary	VARCHAR(20),
        flag_pattern	VARCHAR(20),
        tyres	INTEGER,
        qty_tyres	INTEGER,
        armour	TEXT,
        attack	TEXT,
        qty_attacks	INTEGER,
        fireproof	TEXT,
        insulated	TEXT,
        antibiotic	TEXT,
        banging	TEXT,
        algo	TEXT,
        total_cost	INTEGER,
        user_id INTEGER,
        CONSTRAINT fk_column
        FOREIGN KEY (user_id)
        REFERENCES users (id))"""
  )

print("- Table \"buggies\" exists OK")

con.execute("""
    CREATE TABLE IF NOT EXISTS users (
	id	INTEGER PRIMARY KEY AUTOINCREMENT,
	name	VARCHAR(20),
	username	VARCHAR(20),
	password	VARCHAR(20),
	email	VARCHAR(50),
	is_admin	INTEGER DEFAULT 0
)
""")


cur.execute("SELECT * FROM users LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    gen_password = generate_password_hash('admin')
    cur.execute("INSERT INTO users(name,username,password,email,is_admin) VALUES ('admin','admin',?,'admin@admin.com','1')",(gen_password,))
con.commit()

print("- Table \"users\" exists OK")


con.execute("""
    CREATE TABLE IF NOT EXISTS buggy_costs (
    item TEXT PRIMARY KEY,
	cost_unit	INTEGER,
	cost_kg	INTEGER,
	consumable	TEXT)"""
            )

with open(CSV_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data = []
    for row in csv_reader:
        temp_entry=[]
        for item in row:
            if item == '' or item == None:
                temp_entry.append('')
            else:
                temp_entry.append(item)
        data.append(temp_entry)
    data = tuple(data)
cur.execute("SELECT * FROM buggy_costs LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
    cur.executemany("INSERT INTO buggy_costs VALUES (?,?,?,?)",(data))

    
con.commit()
con.close()
