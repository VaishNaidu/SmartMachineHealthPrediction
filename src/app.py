from src.SMART_MACHINE import SM
from src.common.database import Database
from src.getSymptoms import S
from src.models.user import User
import MySQLdb as sql
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
import random
import string
from datetime import datetime
from datetime import datetime
import matplotlib.pyplot as plt;
import shutil
import webbrowser

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'jslvtr'

from flask import Flask, render_template, request, session

app = Flask(__name__)  # '__main__'
app.secret_key = "secure"


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('patientLogin.html')


@app.route('/register')
def register_template():
    return render_template('patientSignup.html')


@app.route('/auth/reg_base')
def register_basetemp():
    return render_template('register.html')



@app.before_first_request
def initialze_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        name = request.form['email']
        password = request.form['password']
        db = sql.connect("localhost", "root", "", "mini")
        cursor = db.cursor()
        query = "SELECT * from register where email='" + name + "' and password='" + password + "'"
        cursor.execute(query)
        result = cursor.fetchone()


        if result is None:
            return 'Invalid Credentials'

        else:
            print("Logged in!!")
            print(result)
            query2 = "select username from register where email like '"+name+"' ";
            cursor2=db.cursor()
            cursor2.execute(query2)
            result2 = cursor2.fetchone()
            id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            print(id)
            session['email'] = result2
            session['id'] = id
            User.login(name)
            return render_template("profile.html", name=session['name'], email=session['email'], id=session['id'])







@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    dt = datetime.now()
    strg = dt.strftime('%Y')
    print(strg)
    password_again = request.form['password-again']
    if (password == password_again):
        db = sql.connect("localhost", "root", "", "mini")
        cursor = db.cursor()
        sqlqry = "insert into register VALUES('" + name + "','" + email + "','"+password+"','"+strg+"' )"
        cursor.execute(sqlqry)
        db.commit()
        db.close()
        return render_template("patientLogin.html")
    else:
        return "Please Check Your details correctly"




@app.route('/logout')
def logout():
    return render_template("home.html")






@app.route('/adminOne')
def adminOne():
    return render_template("adminlog.html")

@app.route('/adminTwo', methods=['POST'])
def adminTwo():
    return render_template("admin.html")




@app.route('/profile', methods=['POST'])
def symptoms_collect():
    symptom = request.form['symptoms']
    S.add_Symptoms(symptom)
    session['symptom'] = symptom
    # return render_template("profile2.html",symptoms = session['symptom'])
    return render_template("profile.html")


@app.route('/final')
def return_final():
    db = sql.connect("localhost", "root", "", "mini")
    cursor = db.cursor()
    sqlqry = " create table  demo(year varchar(4),total int(5)) as select year, count(*) as total from register group by year ; "
    cursor.execute(sqlqry)
    db.commit()
    sqlqry2="select year from demo"
    cursorTwo=db.cursor()
    cursorTwo.execute(sqlqry2)
    r1=cursorTwo.rowcount
    objects=()
    for x in range(0,r1):
        row=cursorTwo.fetchone()
        objects += (row[0],)


    y_pos = np.arange(len(objects))
    sqlqry3 = "select total from demo"
    cursorThree = db.cursor()
    cursorThree.execute(sqlqry3)
    r2=cursorThree.rowcount
    performance=[]
    objectsTwo=()
    for x in range(0,r2):
        row=cursorThree.fetchone()
        #objectsTwo += (row[0],)
        #r3=str(objectsTwo)
        performance.append(row[0])


    print("Debug Point 2----------------")
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('Programming language usage')
    plt.savefig('graph.jpg', dpi=100)
    sqlqry4 = "drop table demo"
    cursorFour = db.cursor()
    cursorFour.execute(sqlqry4)
    db.close()
    shutil.move("C:\\Users\\HP\\PycharmProjects\\Test\\src\\graph.jpg",
                "C:\\Users\\HP\\PycharmProjects\\Test\\src\\static\\images")

    webbrowser.open("http://localhost:63342/Test/src/templates/output.html")
    return "Success"


@app.route('/symp-final', methods=['POST'])
def return_prediction():
    S.send_Symptoms()
    prediction = SM.predict()

    name = session['name']
    email = session['email']

    id = session['id']
    print(name)
    print(email)
    print(id)
    output=""

    index = 0
    while index < len(email):
        let = email[index]
        if(let=='(' or let==')' or let==','):
            print("")
        else:
            output += let
        index = index + 1

    l=S.length_Symptoms()
    session['len']=l
    print(output)
    session['output']=output;
    c = canvas.Canvas("Report.pdf", pagesize=landscape(letter))
    c.setFont("Helvetica", 14, leading=None)
    # canvas.line(x1,y1,x2,y2)
    c.drawCentredString(30, 500, "Name  :")
    c.drawCentredString(100, 500, name)
    c.showPage()
    c.save()
    if(l>=3):
        session['prediction'] = prediction
        db = sql.connect("localhost", "root", "", "mini")
        query3 = "select hospital from cancer where cancername like '" + prediction + "' ";
        cursor3 = db.cursor()
        cursor3.execute(query3)
        result3 = cursor3.fetchone()
        if result3 is None:
            print("")
        else:

            index = 0
            output2=""
            while index < len(result3):
                let = result3[index]
                if (let == '(' or let == ')' or let == ','):
                    print("")
                else:
                    output2 += let
                index = index + 1

            session['hospital']=output2


    else:
        session['prediction'] = "No Cancer..Please Logout and Enter some more symptoms"
        session['hospital']=None

    return render_template("profile2.html", hospital=session['hospital'], disease=session['prediction'], name=session['name'], output=session['output'], id=session['id'])




if __name__ == '__main__':
    app.run()

