from flask import Flask, render_template, request, session, redirect, url_for, flash
from dbconnect import connectToDB
# from wtforms import Form, TextField, validators, PasswordField

app = Flask(__name__)
app.secret_key = "Hello Session"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login_page')
def login_link():
    return render_template('login.html')


@app.route('/logout')
def logut_page():
    session.pop('email')
    return redirect(url_for('index'))


@app.route('/homepage')
def home_page_link():
    if 'email' in session:
        print "Session found"
        email = session['email']
        connection, cursor = connectToDB()
        cursor.execute("SELECT * FROM student_data WHERE email=%s", (email))
        return render_template('home.html')
    else:
        print "Session not found"
        return redirect(url_for('login_link'))


@app.route('/register', methods=['POST', 'GET'])
def register_data():
    if request.method == 'POST':
        try:
            # Getting Data From Form

            name = request.form['name']
            email = request.form['email']
            mobile_no = request.form['mobile_no']
            gender = request.form['gender']
            pwd = request.form['pwd']
            image = request.form['image']

            # Connection to MySQL
            connection, cursor = connectToDB()
            cursor.execute("INSERT INTO student_data(name, email, mobile, gender, password) VALUES(%s, %s, %s, %s, %s)", (name, email, mobile_no, gender, pwd))
            print "Query"
            connection.commit()
            print "Record Addedd"

        except:
            connection.rollback()
            print "Error.."
        finally:
            return render_template('login.html')
            connection.close()


@app.route('/login', methods=['POST', 'GET'])
def login_data():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        connection, cursor = connectToDB()
        flag = cursor.execute("SELECT * FROM student_data where email=%s and password=%s", (email, pwd))
        print "Record Found"
        if flag:
            print "Redirecting"
            session['email'] = request.form['email']
            print "session started"
            # return render_template('home.html')
            return redirect(url_for('home_page_link'))
            print "Successs"
        else:
            print "Not Found"
            flash("Not Found")
            return redirect(url_for('login_link'))

if __name__ == '__main__':
    app.run()
