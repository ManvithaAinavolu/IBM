from flask import Flask, render_template, request,session,redirect, url_for
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key ='a'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def showall():
    sql= "SELECT * from REGISTER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The username is : ",  dictionary["USERNAME"])
        print("The Password is : ",  dictionary["PASSWORD"])
        print("The Role is : ",  dictionary["ROLE"])
       # print("The Branch is : ",  dictionary["BRANCH"])
       # print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from REGISTER where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The username is : ", dictionary["USERNAME"])
        print("The Password is : ", dictionary["PASSWORD"])
        print("The Role is : ", dictionary["ROLE"])
      #  print("The Branch is : ", dictionary["BRANCH"])
       # print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
def insertdb(conn, name, email, username, password, role):
    role_int = int(role)  # Convert the role value to an integer
    sql = "INSERT into REGISTER VALUES('{}', '{}', '{}', '{}', {})".format(name, email, username, password, role_int)
    print("Insert Query:", sql)  # Print the query for debugging
    stmt = ibm_db.exec_immediate(conn, sql)
    print("Number of affected rows: ", ibm_db.num_rows(stmt))

    
    
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA(1).crt;UID=wrj97286;PWD=yr9TGZdqnKAYr7Tx",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    return render_template('ibm.html')
@app.route('/reg')
def ind():
    return render_template('registration.html')
@app.route('/admin_reg')
def admin_reg():
    return render_template('admin_register.html')
@app.route('/admin_reg', methods=['POST', 'GET'])
def admin_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        #branch = request.form['branch']
       # password = request.form['pwd']

  
        insertdb(conn, name, email, username, password, role)
        return render_template('admin.html', name=name,email=email,username=username,password=password,role=role) 
@app.route('/faculty')
def faculty():
    return render_template('faculty.html')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['pwd']
        role_str = request.form['role']  # Get the role as a string from the form
        
        if role_str == "0":
            role = 0
        elif role_str == "1":
            role = 1
        else:
            role = 2
        
        insertdb(conn, name, email, username, password, role)
        return render_template('login.html')


    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['pwd']
        role = request.form['role']
        if role ==0:
            role = "Faculty"
        elif role==1:
            role = "Student"
        else:
            role="Admin"
        #branch = request.form['branch']
        password = request.form['pwd']
        

        #inp=[name,email,contact,address,role,branch,password]
        insertdb(conn,name,email,username,password,role)
        return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['pwd']
        sql = "select * from REGISTER where email='{}' and password='{}'".format(email, password)
        stmt = ibm_db.exec_immediate(conn, sql)
        userdetails = ibm_db.fetch_both(stmt)
        if userdetails:
            session['register'] = userdetails["EMAIL"]
            role = userdetails["ROLE"]
            if role==0:
                return render_template('faculty.html',  name=userdetails["NAME"],
                  email=userdetails["EMAIL"],
                  username=userdetails["USERNAME"],  
                  password=userdetails["PASSWORD"],
                  role=userdetails['ROLE'])
            elif role==1:
                #session['current_student_id'] = userdetails["STUDENT_ID"]
                return render_template('userprofile.html',name=userdetails["NAME"],
                  email=userdetails["EMAIL"],
                  username=userdetails["USERNAME"],  
                  password=userdetails["PASSWORD"],
                  role=userdetails['ROLE'])
            elif role==2:
                return render_template('admin.html', name=userdetails["NAME"],
                  email=userdetails["EMAIL"],
                  username=userdetails["USERNAME"],  
                  password=userdetails["PASSWORD"],
                  role=userdetails['ROLE'] )
          
        else:
            msg = "Incorrect Email id or Password"
            return render_template("login.html", msg=msg)
    return render_template('login.html')

assignments_data = [
        {
            'assignment_no': 1,
            'assignment_name': 'Assignment 1',
            'due_date': '2023-08-31',
            'submitted_datetime': None,
            'marks': None
        },
        {
            'assignment_no': 2,
            'assignment_name': 'Assignment 2',
            'due_date': '2023-09-15',
            'submitted_datetime': None,
            'marks': None
        }

    ]
def insert_submission(student_id, assignment_no, submission_time):
    sql = "INSERT INTO SUBMIT (STUDENTNAME, ASSIGNMENTNUM, CSUBMITTIME) VALUES (?, ?, ?)"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, student_id)
    ibm_db.bind_param(stmt, 2, assignment_no)
    ibm_db.bind_param(stmt, 3, submission_time)
    ibm_db.execute(stmt)
@app.route('/assignments')
def assignments():
    return render_template('assignments.html', assignments=assignments_data)

@app.route('/submit_assignment/<int:assignment_no>', methods=['POST'])
@app.route('/submit_assignment/<int:assignment_no>', methods=['POST'])
def submit_assignment(assignment_no):
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.pdf'):
            # Generate a unique filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            submission_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            for assignment in assignments_data:
                if assignment['assignment_no'] == assignment_no:
                    assignment['submitted_datetime'] = submission_time
                    break

            submissions_data.append({
                'student_id': session['current_student_id'],  # Use session to retrieve current_student_id
                'assignment_no': assignment_no,
                'assignment_name': assignment['assignment_name'],
                'submission_date': submission_time,
                'marks': None
            })

           # insert_submission(session['current_student_id'], assignment_no, submission_time)

        return redirect(url_for('assignments'))


students_data = [
    {'student_id': 1, 'student_name': 'John'},
    {'student_id': 2, 'student_name': 'Alice'},

]

submissions_data = [
    {'student_id': 1, 'assignment_no': 1, 'assignment_name': 'Assignment 1', 'submission_date': '2023-08-15', 'marks': 0},
    {'student_id': 1, 'assignment_no': 2, 'assignment_name': 'Assignment 2', 'submission_date': '2023-09-01', 'marks': 0},
    
]

@app.route('/facultystulist')
def facultystulist():
    return render_template('facultystulist.html', students=students_data)


@app.route('/facultymarks/<int:student_id>')  # Use a distinct URL pattern for facultymarks
def facultymarks(student_id):
    student_name = None
    student_submissions = []

    for student in students_data:
        if student['student_id'] == student_id:
            student_name = student['student_name']
            break

    for submission in submissions_data:
        if submission['student_id'] == student_id:
            student_submissions.append(submission)

    return render_template('facultymarks.html', student_id=student_id, student_name=student_name, submissions=student_submissions)

# Route to update marks for a specific submission
@app.route('/update_marks/<int:student_id>/<int:assignment_no>', methods=['POST'])
def update_marks(student_id, assignment_no):
    new_marks = int(request.form['marks'])
    for submission in submissions_data:
       if submission['student_id'] == student_id and submission['assignment_no'] == assignment_no:
           submission['marks'] = new_marks
           break
    return redirect(url_for('facultymarks', student_id=student_id))







if __name__ =='__main__':
    app.run( debug = True)
