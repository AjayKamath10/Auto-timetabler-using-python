from flask import Flask, render_template, request
import mysql.connector as sql
import webbrowser as wb
import hashlib


#Connection to MySQL
mydb = sql.connect(host = 'localhost',user = 'root',password = 'TIGER')
def sq(Input):# function to connect to MySQL
    global mydb
    mycur = mydb.cursor()
    mycur.execute(Input)
    mydb.commit()
    
mycur = mydb.cursor()
mycur.execute("USE TIMETABLE1")
#flask
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/log', methods=['GET','POST'])
def my_form_post():
    if request.method == "POST":
        username = str(request.form['uname'])
        print(username)
        password = str(request.form['psw'])
        who = ''

        if username.isdigit():
            who = 't'#teacher
            hashed_passwd = hashlib.md5(password.encode()).hexdigest()
            mycur.execute('select Name from teachers where ID = {} and Password = "{}"'.format(username,hashed_passwd))
            name = mycur.fetchone()
            if name:
               f = name[0] + '.html'
               wb.open(f)
               return render_template('login_success.html')
            else:
                return render_template('login_fail.html')
        elif username == 'admin':
            who = 'a'#admin
            if password == 'admin':
                import TimeTabler
                return render_template('login_success.html')
            else:
                return render_template('login_fail.html')
        else:
            who = 's'#student
            hashed_passwd = hashlib.md5(password.encode()).hexdigest()
            mycur.execute('select class_id from student_login where USN = "{}" and passwd = "{}"'.format(username, hashed_passwd))
            name = mycur.fetchone()
            if name:
                f = name[0] + '.html'
                wb.open(f)
                return render_template('login_success.html')
            else:
                return render_template('login_fail.html')
    
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)





