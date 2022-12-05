from flask import Flask, render_template, request
import pandas as pd
import sqlite3 

app = Flask(__name__)
conn = sqlite3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

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

global data
cur.execute("select * from inventory") 
data = cur.fetchall()
device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
device_id_held = device_id_fetch.fetchall()
conn.commit()

@app.route('/')
def index():
    cur.execute("select * from inventory") 
    data = cur.fetchall()
    return render_template('index.html', value = data)

@app.route('/update.html')
def u():
   return render_template('update.html')


@app.route('/',methods = ['POST', 'GET'])
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
         
         with conn:
            cur.execute(f"""INSERT INTO inventory (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",(d_id,loc,rep,pur,pur_d,acc,cos,loc_f,ser,aud))
            
            conn.commit()
            msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"
      
      finally:
         cur.execute("select * from inventory") 
         data = cur.fetchall()
         global device_id_fetch
         global device_id_held
         device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
         device_id_held = device_id_fetch.fetchall()
         conn.commit()
         return render_template("index.html", value = data)

@app.route('/delete.html')
def d():
   return render_template('delete.html', device_id_display = device_id_held)

@app.route('/r',methods = ['POST', 'GET'])
def delete():
   if request.method == 'POST':
      try:
         i = request.form.get("h")
         with conn:
            sql_delete_query = """DELETE FROM inventory WHERE device_id=?"""
            cur.execute(sql_delete_query, (i,))
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
         return render_template("add.html", value = data)


@app.route('/exist.html')
def e():
   return render_template('exist.html', device_id_display = device_id_held)

@app.route('/exist.html',methods = ['POST', 'GET'])
def exist_show():
   global display_exist
   if request.method == 'POST':
      try:
         global exist_row
         exist_row = request.form.get("exist_row")
         with conn:
            cur.execute("""SELECT * FROM inventory WHERE device_id=?""", (exist_row,))
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
         return render_template("exist.html", display_html_exist = display_exist, device_id_display = device_id_held)


@app.route('/v',methods = ['POST', 'GET'])
def exist():
   if request.method == 'POST':
      try:
         update_id = request.form['d_id']
         update_loc = request.form['loc']
         update_rep = request.form['rep']
         update_pur = request.form['pur']
         update_pur_d = request.form['pur_d']
         update_acc = request.form['acc']
         update_cos = request.form['cos']
         update_loc_f = request.form['loc_f']
         update_ser = request.form['ser']
         update_aud = request.form.get("update_aud")
         update_passw = request.form['pass']
         print(update_aud)
         
         with conn:
            cur.execute(f"""INSERT INTO inventory (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",("d","t","f","v","f","acc","cos","loc_f","ser","aud"))
            #cur.execute(f"""INSERT INTO inventory (device_id, location_status, repair_status, purchase_date, purchase_description, account, cost, location_fixed, serial_number, audit)
             #  VALUES (?,?,?,?,?,?,?,?,?,?)""",(d_id,loc,rep,pur,pur_d,acc,cos,loc_f,ser,aud))
            #''' UPDATE tasks
              #SET priority = ? ,
               #   begin_date = ? ,
                #  end_date = ?
              #WHERE id = ?'''
            conn.commit()
            msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"
      
      finally:
         cur.execute("select * from inventory") 
         data = cur.fetchall()
         global device_id_fetch
         global device_id_held
         device_id_fetch = cur.execute("""SELECT device_id FROM inventory""")
         device_id_held = device_id_fetch.fetchall()
         conn.commit()
         return render_template("send.html", value = data)

if __name__ == "__main__":
    app.run(debug=True)