from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
#TODO 2-RULES - Game rules not setup yet and so cant add validation
#TODO 3-AUTOFILL - rules not set so cant autofill valid data


def form_validation(wheels,power_1,units_1,power_2,units_2,color_1,pattern,color_2):
    wheels=int(wheels)
    if wheels<4 or (wheels%2)!=0 or power_1==power_2 or color_1==color_2 or units_1.isalpha() or not str(units_2).isdigit():
        return 'error'
    elif power_2=="none" and int(units_2)>0:
        return 'error'
    else:
        return 'success'

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
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT qty_wheels,power_type, power_units, aux_power_type, aux_power_units, flag_color_primary, flag_pattern, flag_color_secondary FROM buggies ORDER BY id DESC LIMIT 1")
    record = cur.fetchone()
    value_fills = []
    for data in enumerate(record):
        value_fills.append(data[1])
    if request.method == 'GET':
        return render_template("buggy-form.html",value_fills=value_fills)
    elif request.method == 'POST':
        msg=""
        qty_wheels = request.form['qty_wheels']
        power_type = request.form['power_type']
        power_units = request.form['power_units']
        aux_power_type = request.form['aux_power_type']
        aux_power_units = request.form['aux_power_units']
        flag_color_primary = request.form['flag_color_primary']
        flag_pattern = request.form['flag_pattern']
        flag_color_secondary = request.form['flag_color_secondary']
        if not qty_wheels:
            qty_wheels = '4'
        elif not power_units:
            power_units='1'
        if not aux_power_units:
            aux_power_units=0
        if form_validation(qty_wheels, power_type, power_units, aux_power_type, aux_power_units, flag_color_primary, flag_pattern, flag_color_secondary) == 'error':
            msg="error in update operation"
            fix_entry=True
            return render_template("updated.html", msg=msg,fix_entry=fix_entry)
            #TODO find some way of leaving user data in forms if there is an incomplete buggy submit
        else:
            try:
                msg = f"qty_wheels={qty_wheels}"
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("SELECT id FROM buggies ORDER BY id DESC LIMIT 1")
                    latest_id = cur.fetchone()
                    cur.execute(
                        "INSERT INTO buggies (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, flag_color_primary, flag_pattern, flag_color_secondary) VALUES(?,?,?,?,?,?,?,?)",
                        (qty_wheels, power_type, power_units, aux_power_type, aux_power_units, flag_color_primary,
                         flag_pattern, flag_color_secondary))
                    # cur.execute("UPDATE buggies set qty_wheels=?, power_type=?,power_units=?,aux_power_type=?,aux_power_units=?,flag_color_primary=?,flag_pattern=?,flag_color_secondary=? WHERE id=?", (qty_wheels,power_type,power_units,aux_power_type,aux_power_units,flag_color_primary,flag_pattern,flag_color_secondary, DEFAULT_BUGGY_ID))
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
    #elif request.method == 'POST':
    #TODO finish setting up passthrough from manage to edit buggy


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
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
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
def delete_buggy():
    try:
        msg = "deleting buggy"
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM buggies")
            con.commit()
            msg = "Buggy deleted"
    except:
        con.rollback()
        msg = "error in delete operation"
    finally:
        con.close()
        return render_template("updated.html", msg = msg)


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
