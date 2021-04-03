from flask import Flask, render_template, request,jsonify,redirect,flash,session
import MySQLdb
from MySQLdb.cursors import DictCursor
import prediction
app = Flask(__name__)
app.secret_key="secret"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aditya@123'
app.config['MYSQL_DB'] = 'easy_detect'
db_connect=MySQLdb.connect('freedb.tech','freedbtech_Finalproject','AAACV123','freedbtech_easydetect')
cur = db_connect.cursor(cursorclass=DictCursor)`
`
@app.route('/', methods=['GET'])
def index():
    if "loggedin" in session.keys() and session['loggedin']:
        return redirect('/welcome')
    else:
        session['loggedin']=False
        print("check1")
        return render_template('login1.html')
@app.route('/register',methods=['GET'])
def get_register():
    return render_template('register.html')
@app.route('/login',methods=['GET'])
def get_login():
    if session['loggedin']:
        return redirect('/welcome')
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
    if session['loggedin']:
        redirect('/welcome')
    username=request.form['username']
    password=request.form['password']
    login_type=request.form['login_type']
    if login_type == 'patient':
        quey="select * from patient where username='"+username+"' and password='"+password+"'"
    else:
        quey="select * from doctor where username='"+username+"' and password='"+password+"'"
    print(quey)
    cur.execute(quey)
    data=cur.fetchall()
    if len(data)==0:
        print("checking login")
        flash('enter valid data')
        return redirect('/')
    #print(jsonify(cur.fetchall()))
    session['data']=data
    session['loggedin']=True
    return redirect('/welcome')
@app.route('/welcome',methods=['GET'])
def welcome():
    return session['data'][0]
@app.route('/register',methods=['POST'])
def register():
    specialization=None
    table_name=request.form['signup_type']
    username=request.form['username']
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    age=int(request.form['age'])
    address=request.form['address']
    phone=int(request.form['phone'])
    if table_name == 'doctor':
        specialization=request.form['specialization']
    password=request.form['password']
    if table_name=="doctor":
        cur.execute("insert into "+table_name+"(username,firstname,lastname,age,address,phone,specialization,password) values(%s,%s,%s,%s,%s,%s,%s,%s);",(username,firstname,lastname,int(age),address,int(phone),specialization,password))
    if table_name=="patient":
        cur.execute("insert into "+table_name+"(username,firstname,lastname,age,address,phone,password) values(%s,%s,%s,%s,%s,%s,%s);",(username,firstname,lastname,int(age),address,int(phone),password))

    db_connect.commit()
    return redirect('/')
@app.route('/logout',methods=['GET'])
def logout():
    session['loggedin']=False
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)
