from flask import Flask, render_template
import pandas as pd
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect('inventory.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
   device_id  TEXT NULL,
   location_status TEXT NULL,
   repair_status  TEXT NULL,
   purchase_date  TEXT NULL,
   purchase_description  TEXT NULL,
   account  TEXT NULL,
   cost  INT NULL,
   location_fixed  TEXT NULL,
   serial_number  TEXT NULL,
   audit  TEXT NULL
);
""")

cur.execute("""INSERT INTO inventory VALUES
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
cur.execute("select * from inventory") 
data = cur.fetchall()
conn.close()

@app.route('/')
def index():
    return render_template('index.html', value=data)


if __name__ == "__main__":
    app.run(debug=True)