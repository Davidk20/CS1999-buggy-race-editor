from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, Blueprint
from flask_login import login_required,current_user
import sqlite3 as sql
from form_validation import buggy_validation
from cost_method import cost_method
from fill_form import fill_form
main = Blueprint('main',__name__)
DATABASE_FILE = "database.db"
BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
value_fills=[]
new_buggy=[]
updated_id=0
#TODO after deleting buggies, fix counter for id so that buggies will always fill current gaps

#TODO add tooltips onto forms
#TODO custom 404 page


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@main.route('/')
def home():
    try:
        name = current_user.name
    except AttributeError:
        name = "Guest"
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, name=name)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@main.route('/new', methods = ['POST', 'GET'])
def create_buggy():
    if request.method == 'GET':
        buggy_class = fill_form(None)
        value_fills = buggy_class.random_buggy()
        return render_template("buggy-form.html",value_fills=value_fills)
    elif request.method == 'POST':
        msg=""
        new_buggy=[]
        for parameter in ['qty_wheels','power_type','power_units','aux_power_type','aux_power_units','hamster_booster','flag_color_primary','flag_pattern','flag_color_secondary','tyres','qty_tyres','armour','attack','qty_attacks','fireproof','insulated','antibiotic','banging','algo']:
            result = request.form.get(parameter)
            new_buggy.append(result)
        result = buggy_validation(new_buggy)
        total = cost_method(new_buggy)
        cost = total.buggy_cost()
        costs = str(cost[0])+' / '+str(cost[1])
        new_buggy.append(costs)
        try:
            new_buggy.append(current_user.id)
        except AttributeError:
            buggy_class = fill_form(new_buggy)
            value_fills = buggy_class.fill_form()
            flash('You are not logged in, please login to save a buggy', 'warning')
            return render_template("buggy-form.html", value_fills=value_fills)
        if result.passback() == 'error':
            buggy_class = fill_form(new_buggy)
            value_fills = buggy_class.fill_form()
            flash('There is an error in the input of the buggy, please try again', 'warning')
            return render_template("buggy-form.html", value_fills=value_fills)
        elif result.passback() == 'success':
            try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO buggies (qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo,total_cost,user_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[new_buggy[0],new_buggy[1],new_buggy[2],new_buggy[3],new_buggy[4],new_buggy[5],new_buggy[6],new_buggy[7],new_buggy[8],new_buggy[9],new_buggy[10],new_buggy[11],new_buggy[12],new_buggy[13],new_buggy[14],new_buggy[15],new_buggy[16],new_buggy[17],new_buggy[18],new_buggy[19],new_buggy[20],])
                    con.commit()
                    msg = "Record successfully saved"
            except:
                con.rollback()
                msg = "error in update operation"
            finally:
                con.close()
                return render_template("updated.html", msg = msg, fix_entry=False, deleted=True)



@main.route('/update', methods = ['POST', 'GET'])
def update_buggy():
    if request.method == 'POST':
        msg=""
        new_buggy=[]
        for parameter in ['qty_wheels','power_type','power_units','aux_power_type','aux_power_units','hamster_booster','flag_color_primary','flag_pattern','flag_color_secondary','tyres','qty_tyres','armour','attack','qty_attacks','fireproof','insulated','antibiotic','banging','algo']:
            result = request.form.get(parameter)
            new_buggy.append(result)
        result = buggy_validation(new_buggy)
        total = cost_method(new_buggy)
        cost = total.buggy_cost()
        costs = str(cost[0])+' / '+str(cost[1])
        new_buggy.append(costs)
        if result.passback() == 'error':
            msg="error in update operation - Invalid Buggy configured"
            fix_entry=True
            return render_template("updated.html", msg=msg,fix_entry=fix_entry)
            #TODO find some way of leaving user data in forms if there is an incomplete buggy submit
        elif result.passback() == 'success':
            #try:
                with sql.connect(DATABASE_FILE) as con:
                    cur = con.cursor()
                    cur.execute("UPDATE buggies SET qty_wheels=?,power_type=?,power_units=?,aux_power_type=?,aux_power_units=?,hamster_booster=?,flag_color_primary=?,flag_pattern=?,flag_color_secondary=?,tyres=?,qty_tyres=?,armour=?,attack=?,qty_attacks=?,fireproof=?,insulated=?,antibiotic=?,banging=?,algo=?,total_cost=? WHERE id=?",([new_buggy[0],new_buggy[1],new_buggy[2],new_buggy[3],new_buggy[4],new_buggy[5],new_buggy[6],new_buggy[7],new_buggy[8],new_buggy[9],new_buggy[10],new_buggy[11],new_buggy[12],new_buggy[13],new_buggy[14],new_buggy[15],new_buggy[16],new_buggy[17],new_buggy[18],new_buggy[19],updated_id]))
                    con.commit()
                    msg = "Record successfully saved"
            #except:
             #   con.rollback()
             #   msg = "error in update operation"
            #finally:
                con.close()
                return render_template("updated.html", msg = msg, fix_entry=False, deleted=True)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------


@main.route('/buggy', methods = ['POST', 'GET'])
@login_required
def show_buggies():
    if request.method == 'GET':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT id,qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_color_secondary,flag_pattern,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo,total_cost FROM buggies WHERE user_id=?",(current_user.id,))
        record = cur.fetchall()
        return render_template("buggy.html", buggy = record)
    elif request.method == 'POST':
        command = request.form
        command_list=[]
        for key, value in command.items():
            temp = [key, value]
            command_list.append(temp)
        if command_list[0][1] == 'Modify':
            buggy = fill_form(command_list[0][0])
            global updated_id
            updated_id=command_list[0][0]
            return render_template("buggy_update.html", value_fills=buggy)
        elif command_list[0][1] == 'Delete':
            msg = delete_buggy(command_list[0][0])
            return render_template("updated.html", msg=msg, deleted=True)
        elif command_list[0][1] == 'graphic':
            flag_vars=display_graphic(command_list[0][0])
            return render_template("graphic.html", flag_vars=flag_vars)
#TODO create custom div for user to view flags using template patterns and pass colours through from list into the styles

#------------------------------------------------------------
# a page for displaying the buggy form
#------------------------------------------------------------





#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------


@main.route('/json')
@login_required
def summary():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo FROM buggies WHERE user_id=? ORDER BY id DESC LIMIT 1",(current_user.id,))
    try:
        return jsonify(
            {k: v for k, v in dict(zip(
              [column[0] for column in cur.description], cur.fetchone())).items()
              if (v != "" and v is not None)
            }
          )
    except TypeError:
        flash('No records found, please create a buggy before requesting JSON')
        return render_template('index.html')
#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------


@main.route('/delete')
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


@main.route('/graphic')
def display_graphic(buggy_id):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT flag_color_primary,flag_pattern,flag_color_secondary FROM buggies WHERE id=?", (buggy_id,))
    result = cur.fetchall();
    flag_vars = [result[0][0], result[0][1], result[0][2]]
    flag_vars = [flag_vars[1], flag_vars[0], flag_vars[2]]
    return flag_vars
    #return render_template("graphic.html",flag_vars=flag_vars)

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")

#TODO wrap button in a tag to simletaneously trigger and submit the submitted id into varioable so i can use it to choose which flag to render