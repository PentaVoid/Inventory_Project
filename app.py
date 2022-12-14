from flask import Flask, render_template, request
import pandas as pd
import sqlite3 

#initialize flask app, database and main database variables
app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

#Create table headers
conn.execute("""CREATE TABLE IF NOT EXISTS inventory (
   device_id  TEXT NULL,
   location_status TEXT NULL,
   repair_status  TEXT NULL,
   purchase_date  TEXT NULL,
   purchase_description  TEXT NULL,
   account  TEXT NULL,
   cost  INT NULL,
   location_fixed  TEXT NULL,
   serial_number  TEXT NULL,
   audit  TEXT NULL,
   UNIQUE (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit) ON CONFLICT IGNORE
);
""")
conn.commit()

#Base table values (STEM-MINDS 1-19)
conn.execute("""INSERT INTO inventory (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit)
 VALUES
('STEMMINDS-001','repair','hello','2017-12-01','STEMSTUDENT-001','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040E88C6600','Item Found'),
('STEMMINDS-002','','','2017-12-01','STEMSTUDENT-002','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e94d6600','Item Found'),
('STEMMINDS-003','','','2017-12-01','STEMSTUDENT-003','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e93a6600','Item Found'),
('STEMMINDS-004','','','2017-12-01','STEMSTUDENT-004-write-off','10500 - Computers - Student Use',250,'Earl Stewart Dr','XMRWAA0045040E9196600','Write-off'),
('STEMMINDS-005','','','2017-12-01','STEMSTUDENT-005','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e91d6600','Item Found'),
('STEMMINDS-006','','','2017-12-01','STEMSTUDENT-006','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA004504101816600','Item Found'),
('STEMMINDS-007','','','2017-12-01','STEMSTUDENT-007','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e8946600','Item Found'),
('STEMMINDS-008','','','2017-12-01','STEMSTUDENT-008','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045041011b6600','Item Found'),
('STEMMINDS-009','','','2017-12-01','STEMSTUDENT-009','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e93d6600','Item Found'),
('STEMMINDS-010','','','2017-12-01','STEMSTUDENT-010-write-off','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA004504102966600','Write-off'),
('STEMMINDS-011','','','2017-12-01','STEMSTUDENT-011','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040E9606600','Item Found'),
('STEMMINDS-012','','','2017-12-01','STEMSTUDENT-012','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040e9366600','Item Found'),
('STEMMINDS-013','','','2017-12-01','STEMSTUDENT-013','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXRMWAA0045040e8ca6600','Item Found'),
('STEMMINDS-014','','','2017-12-01','STEMSTUDENT-014','10500 - Computers - Student Use',250,'writeoff-2021','NXMRWAA0045040e92c6600','Need to find'),
('STEMMINDS-015','','','2017-12-01','STEMSTUDENT-015-write-off','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040E89E6600','Write-off'),
('STEMMINDS-016','','','2017-12-01','STEMSTUDENT-016','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040E8BB6600','Item Found'),
('STEMMINDS-017','','','2017-12-01','STEMSTUDENT-017','10500 - Computers - Student Use',250,'Earl Stewart Dr','NXMRWAA0045040E9436600','Item Found'),
('STEMMINDS-018','','','2017-12-01','STEMOFFICE-8','10400 - Computers - Office Use',250,'In Closet','CND6381WV5','Item Found'),
('STEMMINDS-019','','','2017-12-01','STEMOFFICE-7','10400 - Computers - Office Use',250,'LAHIQA','CND6382SSS','Need to find');"""
)
conn.commit()

#define data holds all table data, and device_id_held holds device id data
global data
cur.execute("select * from inventory") 
data = cur.fetchall()
device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
device_id_held = device_id_fetch.fetchall()
conn.commit()

#home page
@app.route('/index.html')
def index():
    cur.execute("select * from inventory") 
    data = cur.fetchall()
    return render_template('index.html', value = data)

#update page
@app.route('/update.html')
def u():
   return render_template('update.html')

#update form to allow new table values
@app.route('/index.html',methods = ['POST', 'GET'])
def update():
   if request.method == 'POST':
      try:
         d_id = request.form['d_id']
         loc = request.form['loc']
         rep = request.form['rep']
         pur = request.form['pur']
         pur_d = request.form['pur_d']
         acc = request.form['acc']
         cos = request.form['cos']
         loc_f = request.form['loc_f']
         ser = request.form['ser']
         aud = request.form['aud']
         passw = request.form['pass']
         print(d_id)
         with conn:
            cur.execute(f"""INSERT INTO inventory (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",(d_id,loc,rep,pur,pur_d,acc,cos,loc_f,ser,aud))
            
            conn.commit()
            msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"
      
      finally:
         #update data variables with new changes
         cur.execute("select * from inventory") 
         data = cur.fetchall()
         global device_id_fetch
         global device_id_held
         device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
         device_id_held = device_id_fetch.fetchall()
         conn.commit()
         return render_template("index.html", value = data)

#delete page
@app.route('/delete.html')
def d():
   return render_template('delete.html', device_id_display = device_id_held)

#delete form to delete rows
@app.route('/r',methods = ['POST', 'GET'])
def delete():
   if request.method == 'POST':
      try:
         delete_row = request.form.get("delete_row")
         with conn:
            sql_delete_query = """DELETE FROM inventory WHERE device_id=?"""
            cur.execute(sql_delete_query, (delete_row,))
            conn.commit()
      except:
         conn.rollback()
      
      finally:
         cur.execute("select * from inventory") 
         data = cur.fetchall()
         global device_id_fetch
         global device_id_held
         device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
         device_id_held = device_id_fetch.fetchall()
         conn.commit()
         return render_template("time_space.html", value = data)


#update existing page
@app.route('/exist.html')
def e():
   return render_template('exist.html', device_id_display = device_id_held)

#existing form to display chosen row
@app.route('/exist.html',methods = ['POST', 'GET'])
def exist():
   if request.method == 'POST':
      try:
         global exist_row
         exist_row =  request.form.get("exist_row")
         with conn:
            cur.execute("""SELECT * FROM inventory WHERE device_id=?""", (exist_row,))
            global display_exist
            display_exist = cur.fetchall()
            conn.commit()
      except:
         conn.rollback()
      
      finally:
         cur.execute("select * from inventory") 
         data = cur.fetchall()
         global device_id_fetch
         global device_id_held
         device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
         device_id_held = device_id_fetch.fetchall()
         conn.commit()
         return render_template("exist.html", display_html_exist = display_exist, device_id_display = device_id_held, value = data)


         
#existing form to update chosen row
@app.route('/exist_complete.html',methods = ['POST', 'GET'])
def exists():
      if request.method == 'POST':
         try:
            update_id = request.form['update_id']
            update_loc = request.form['update_loc']
            update_rep = request.form['update_rep']
            update_pur = request.form['update_pur']
            update_pur_d = request.form['update_pur_d']
            update_acc = request.form['update_acc']
            update_cos = request.form['update_cos']
            update_loc_f = request.form['update_loc_f']
            update_ser = request.form['update_ser']
            update_aud = request.form.get("update_aud")
            print(update_id)
            print(update_acc)
            with conn:
               sql_update_query =''' UPDATE inventory
               SET device_id = ?, 
               location_status = ?,
               repair_status = ?,
               purchase_date = ?,
               purchase_description = ?,
               account = ?,
               cost = ?,
               location_fixed = ?,
               serial_number = ?,
               audit = ?
               WHERE device_id = ? 
               '''
               v = exist_row
               params = (update_id, update_loc, update_rep, update_pur, update_pur_d, update_acc, update_cos, update_loc_f, update_ser, update_aud, v)
               cur.execute(sql_update_query, params)
               conn.commit()
         except:
            print("error")
         finally:
            global display_exist
            display_exist = cur.fetchall()
            cur.execute("select * from inventory") 
            data = cur.fetchall()
            global device_id_fetch
            global device_id_held
            device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
            device_id_held = device_id_fetch.fetchall()
            conn.commit()
            return render_template("time_space.html", display_html_exist = display_exist, device_id_display = device_id_held, value = data)
if __name__ == "__main__":
    app.run(debug=True)