from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, Blueprint
from flask_login import login_required,current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
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


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@main.route('/')
def home():
    try:
        name = current_user.name
        is_admin = current_user.is_admin()
    except AttributeError:
        name = "Guest"
        is_admin = 0
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, name=name, is_admin=is_admin)

#------------------------------------------------------------
# new buggy form
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
    if request.method == 'GET':
        return render_template("buggy-form.html")
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
# table of all buggies
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
            buggy_class = fill_form(int(command_list[0][0]))
            value_fills = buggy_class.fill_form()
            return render_template("buggy_update.html", value_fills=value_fills)
        elif command_list[0][1] == 'Delete':
            msg = delete_buggy(command_list[0][0])
            return render_template("updated.html", msg=msg, deleted=True)
        elif command_list[0][1] == 'JSON':
            con = sql.connect(DATABASE_FILE)
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute(
                "SELECT qty_wheels,power_type,power_units,aux_power_type,aux_power_units,hamster_booster,flag_color_primary,flag_pattern,flag_color_secondary,tyres,qty_tyres,armour,attack,qty_attacks,fireproof,insulated,antibiotic,banging,algo FROM buggies WHERE user_id=? and id=?",
                (current_user.id, command_list[0][0]))
            return jsonify(
                {k: v for k, v in dict(zip(
                    [column[0] for column in cur.description], cur.fetchone())).items()
                 if (v != "" and v is not None)
                 }
            )


#------------------------------------------------------------
# delete the buggy
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


#------------------------------------------------------------
# display flag graphic
#------------------------------------------------------------
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


#------------------------------------------------------------
# admin page for managing users
#------------------------------------------------------------
@main.route('/manage',methods = ['POST', 'GET'])
@login_required
def manage_users():
    if request.method == "GET":
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT id,name,username,email FROM users")
        result = cur.fetchall();
        return render_template("manage_users.html", users = result)
    elif request.method == "POST":
        command = request.form
        command_list = []
        for key, value in command.items():
            temp = [key, value]
            command_list.append(temp)
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT id,name,username,email FROM users")
        result = cur.fetchall()
        if command_list[0][1] == 'Reset Password':
            new_pass = generate_password_hash('Pass1234')
            cur.execute("UPDATE users SET password=? WHERE id=?",(new_pass,command_list[0][0]))
            con.commit()
            flash('Password reset, New password = Pass1234')
            return render_template("manage_users.html", users = result)
        elif command_list[0][1] == 'Make Admin':
            cur.execute("UPDATE users SET is_admin=1 WHERE id=?",(command_list[0][0],))
            con.commit()
            flash('User is now admin')
            return render_template("manage_users.html", users = result)
        elif command_list[0][1] == 'Delete User':
            try:
                cur.execute("DELETE FROM users WHERE id=?", (command_list[0][0],))
                con.commit()
                flash('User Deleted')
            except:
                con.rollback()
            finally:
                cur.execute("SELECT id,name,username,email FROM users")
                result = cur.fetchall()
                con.close()
                return render_template("manage_users.html",users = result)


#------------------------------------------------------------
# personal user management page
#------------------------------------------------------------
@main.route('/personal',methods = ['POST', 'GET'])
@login_required
def manage_account():
    if request.method == "GET":
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT id,name,username,email FROM users WHERE id=?",(int(current_user.id),))
        result = cur.fetchall();
        return render_template("manage_account.html",users = result)
    elif request.method == 'POST':
        con = sql.connect(DATABASE_FILE)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?",(int(current_user.id),))
        result = cur.fetchone();
        cur.execute("SELECT id,name,username,email FROM users WHERE id=?",(int(current_user.id),))
        results = cur.fetchall()
        command = request.form
        command_list=[]
        for key, value in command.items():
            temp = [key, value]
            command_list.append(temp)
        if command_list[0][1] == 'Delete Account':
            try:
                cur.execute("DELETE FROM users WHERE id=?", (command_list[0][0],))
                con.commit()
            except:
                con.rollback()
            finally:
                con.close()
                logout_user()
                flash('Account Deleted, you have been logged out.')
                return render_template("index.html")
        elif command_list[0][0] == 'name':
            updates=[]
            print('yes')
            for item in range(len(command_list)):
                if command_list[item][1] != '':
                    updates.append(command_list[item])
                else:
                   updates.append([command_list[item][0],result[item+1]])
            print(updates)
            if command_list[3][1] != command_list[4][1]:
                flash("Error - Password doesn't match")
                return render_template('manage_account.html',users = results)
            elif not check_password_hash(result[3],command_list[3][1]):
                flash("Error - Incorrect Password")
                return render_template('manage_account.html',users = results)
            else:
                cur.execute("SELECT * FROM users")
                accounts = cur.fetchall()
                for user in range(len(accounts)):
                    if command_list[1][1] == accounts[user][2]:
                        flash('Account name already in use', 'warning')
                        return render_template('manage_account.html', users=results)
                    elif command_list[2][1] == accounts[user][4]:
                        flash('Email Address already in use', 'warning')
                        return render_template('manage_account.html', users=results)
                cur.execute("UPDATE users SET name=?,username=?,email=? WHERE id=?",(updates[0][1],updates[1][1],updates[2][1],result[0]))
                con.commit()
                cur.execute("SELECT id,name,username,email FROM users WHERE id=?", (int(current_user.id),))
                result = cur.fetchall()
                return render_template("manage_account.html", users=result)

        elif command_list[0][0] == 'old_password':
            if not check_password_hash(result[3],command_list[0][1]):
                flash("Error - Incorrect Password")
                return render_template('manage_account.html',users = results)
            elif command_list[1][1] != command_list[2][1]:
                flash("Error - Password doesn't match")
                return render_template('manage_account.html',users = results)
            else:
                new_password = generate_password_hash(command_list[1][1])
                cur.execute("UPDATE users SET password=? WHERE id=?",(new_password,result[0]))
                con.commit()
                cur.execute("SELECT id,name,username,email FROM users WHERE id=?", (int(current_user.id),))
                result = cur.fetchall()
                flash("Password successfully changed")
                return render_template("manage_account.html", users=result)


#------------------------------------------------------------
# poster page
#------------------------------------------------------------
@main.route('/poster')
def poster():
   return render_template('poster.html')


#------------------------------------------------------------
# Race Results
#------------------------------------------------------------
@main.route('/results')
def results():
   return render_template('results.html')


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")
