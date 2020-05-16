from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"



def form_validation(wheels,power_1,units_1,power_2,units_2,color_1,pattern,color_2):
  for require in [wheels,power_1,units_1,power_2,units_2,color_1,pattern,color_2]:
    if require=='' or ' ':
      return 'error'
  wheels=int(wheels)
  if wheels<4 or (wheels%2)!=0 or power_1==power_2 or color_1==color_2 or units_1.isalpha() or units_2.isalpha():
    return 'error'
  elif power_2=="none" and int(units_2)>0:
    return 'error'
  elif power_2!='none' and int(units_2)<1:
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
  if request.method == 'GET':
    return render_template("buggy-form.html")
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
    if form_validation(qty_wheels, power_type, power_units, aux_power_type, aux_power_units, flag_color_primary, flag_pattern, flag_color_secondary) == 'error':
      print('error')
      msg="error in update operation"
      fix_entry=True
      return render_template("updated.html", msg=msg,fix_entry=fix_entry)
    else:
      try:
        msg = f"qty_wheels={qty_wheels}"
        with sql.connect(DATABASE_FILE) as con:
          cur = con.cursor()
          cur.execute("UPDATE buggies set qty_wheels=?, power_type=?,power_units=?,aux_power_type=?,aux_power_units=?,flag_color_primary=?,flag_pattern=?,flag_color_secondary=? WHERE id=?", (qty_wheels,power_type,power_units,aux_power_type,aux_power_units,flag_color_primary,flag_pattern,flag_color_secondary, DEFAULT_BUGGY_ID))
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
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone(); 
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
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
