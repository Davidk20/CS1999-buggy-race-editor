from flask import Flask, render_template, request, jsonify, g
import sqlite3 as sql
from form_validation import buggy_validation
import random
app = Flask(__name__)
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
value_fills=[]
new_buggy=[]
#TODO 2-RULES - Game rules not setup yet and so cant add validation
#TODO 3-AUTOFILL - rules not set so cant autofill valid data


def fill_form(buggy):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    if buggy == None:
        cur.execute("SELECT qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo FROM buggies ORDER BY id DESC LIMIT 1")
    else:
        cur.execute("SELECT qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo FROM buggies WHERE id=?",(buggy,))
    record = cur.fetchone()
    value_fills = []
    try:
        for data in enumerate(record):
            value_fills.append(data[1])
    except:
        value_fills=[]
    return value_fills
#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        value_fills = fill_form(None)
        return render_template("buggy-form.html",value_fills=value_fills)
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        hamster_booster = request.form['hamster_booster']
        flag_color_primary = request.form['flag_color_primary']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']
        tyres = request.form['tyres']
        qty_tyres = request.form['qty_tyres']
        armour = request.form['armour']
        attack = request.form['attack']
        qty_attacks = request.form['qty_attacks']
        fireproof = request.form['fireproof']
        insulated = request.form['insulated']
        antibiotic = request.form['antibiotic']
        banging = request.form['banging']
        algo = request.form['algo']
        new_buggy=[qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo]
        result = buggy_validation(new_buggy)
        if result.passback() == 'error':
            msg="error in update operation"
            fix_entry=True
            return render_template("updated.html", msg=msg,fix_entry=fix_entry)
            #TODO find some way of leaving user data in forms if there is an incomplete buggy submit
        elif result.passback() == 'success':
            try:
                msg = f"qty_wheels={qty_wheels}"
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("SELECT id FROM buggies ORDER BY id DESC LIMIT 1")
                    latest_id = cur.fetchone()
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo))
                    con.commit()
                    msg = "Record successfully saved"
            except:
              con.rollback()
              msg = "error in update operation"
            finally:
              con.close()
            return render_template("updated.html", msg = msg, fix_entry=False)


#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------


@app.route('/buggy', methods = ['POST', 'GET'])
def show_buggies():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM buggies")
        record = cur.fetchall();
        return render_template("buggy.html", buggy = record)
    elif request.method == 'POST':
        command = request.form
        command_list=[]
        for key, value in command.items():
            temp = [key, value]
            command_list.append(temp)
        print(command_list[0][1])
        if command_list[0][1] == 'Modify':
            buggy = fill_form(command_list[0][0])
            return render_template("buggy-form.html", value_fills=buggy)
        elif command_list[0][1] == 'Delete':
            msg = delete_buggy(command_list[0][0])
            return render_template("updated.html", msg=msg, deleted=True)
#TODO create custom div for user to view flags using template patterns and pass colours through from list into the styles

#------------------------------------------------------------
# a page for displaying the buggy form
#------------------------------------------------------------


@app.route('/new')
def edit_buggy():
    return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------


@app.route('/json')
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=10 LIMIT 1")
    return jsonify(
        {k: v for k, v in dict(zip(
          [column[0] for column in cur.description], cur.fetchone())).items()
          if (v != "" and v is not None)
        }
      )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------


@app.route('/delete', methods = ['POST'])
def delete_buggy(buggy_id):
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
            con.commit()
            msg = "Buggy Deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return msg


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
