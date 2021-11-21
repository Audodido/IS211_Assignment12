from flask import Flask, session, redirect, url_for, request, render_template, current_app, g
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('hw13.db') #connect to the database
cur = conn.cursor() 

check_username = 'admin'
check_password = 'password'
app.secret_key = '\xbb\xcc\xdbS-\xcb\x99\xc3\xf5\xe7&\x87\xcc\xef\x98\x86\x80[\xcd\xad\x05\xf6\xfd\xd2'



students = {
    1 : ['John', 'Smith'],
    2 : ['Connor', 'Hanwick'],
    3 : ['Miles', 'Davis']
}

quizzes = {
    1 : ['Python Basics', 5, 'February, 5, 2015'],
    2 : ['Web App Development', 15, 'March, 10, 2015']
}

quiz_results = {
    1: [1, 1, 85]
}


#clear tables each time program is run - might remove
for i in ('students','quizzes','quiz_results'):
    cur.execute(f'DROP TABLE IF EXISTS {i}')


#create tables 
cur.execute('''CREATE TABLE IF NOT EXISTS students ( 
            first_name TEXT,
            last_name TEXT
            )''')
cur.execute('''CREATE TABLE IF NOT EXISTS quizzes (
            subject_ TEXT,
            number_of_questions INT,
            date_given TEXT
            )''')
cur.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            student_id INTEGER,
            quiz_id INTEGER,
            score INTEGER
            )''')

def populate_table(dict, table):
    #add student data to table 
    for k, v in dict.items():
        if table == 'students':
            cur.execute(f'INSERT INTO {table} VALUES (?,?)', (v))
        else: 
            cur.execute(f'INSERT INTO {table} VALUES (?,?,?)', (v))
    conn.commit()

# #populate tables 
populate_table(students, 'students')
populate_table(quizzes, 'quizzes')
populate_table(quiz_results, 'quiz_results')


# sitebuilding - sitebuilding - sitebuilding - sitebuilding - sitebuilding - sitebuilding 


@app.route('/')
def main_page():
    return redirect('/login')

#https://stackoverflow.com/questions/13326599/how-can-i-set-the-current-session-as-logged-in-using-python-in-flask-with-flas
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != check_username:
            error = 'Incorrect username'
        elif request.form['password'] != check_password:
            error = 'Incorrect password'
        else:
            session['logged_in'] = True 
            return redirect(url_for('dashboard'))

    return render_template('login.html', error=error)

#All subsequent controllers should check if the request is being made by a logged in user.

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('hw13.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 
    if session['logged_in'] == True:
        cur.execute('''SELECT rowid, first_name, last_name FROM students''')
        students = cur.fetchall()
        cur.execute('''SELECT rowid, subject_, number_of_questions, date_given FROM quizzes''')
        quizzes = cur.fetchall()
        return render_template('dashboard.html', students=students, quizzes=quizzes)



@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    error=None
    conn = sqlite3.connect('hw13.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('studentadd.html')
        elif request.method == 'POST':
            first = request.form['first_name'] 
            last = request.form['last_name']
            cur.execute('INSERT INTO students VALUES (?,?)', (first, last))
            conn.commit()
            # print(first,last, 'added to \'students\' table')
            return redirect('/dashboard')
        else:
            error = "An error occurred adding this student. Try again."
            return render_template('studentadd.html', error=error)
    else: 
        error = 'You must log in to continue'
        return render_template('login.html', error=error)


@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    error=None
    conn = sqlite3.connect('hw13.db') #connect to the database in same thread/method !!change to g.db!!
    cur = conn.cursor() 
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('quizadd.html')
        elif request.method == 'POST':
            subject = request.form['subject']
            qnum = request.form['qnum']
            date = f"{request.form['month_day']}, {request.form['year']}"
            cur.execute('INSERT INTO quizzes VALUES (?,?,?)', (subject, qnum, date))
            conn.commit()
            return redirect('/dashboard')
        else:
            error = "An error occurred adding this quiz. Try again."
            return render_template('quizadd.html', error=error)
    else: 
        error = 'You must log in to continue'
        return render_template('login.html', error=error)



if __name__ == '__main__':

    app.run(debug=True)    







    # # print(quiz_results(1, 85))
    # results = []
    # cur.execute('''SELECT * FROM students''')
    # results.append(cur.fetchall())
    # cur.execute('''SELECT * FROM quizzes''')
    # results.append(cur.fetchall())
    # cur.execute('''SELECT qr.score,
    #             s.first_name
    #             FROM quiz_results qr
    #             JOIN students s
    #             ON qr.student_id = s.id''')
    # results.append(cur.fetchall())
    
    # for r in results:
    #     print(r)