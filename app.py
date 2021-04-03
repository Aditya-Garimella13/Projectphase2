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
db_connect=MySQLdb.connect('remotemysql.com','XFio3uevxr','DrOzBUgBwI','XFio3uevxr')
cur = db_connect.cursor(cursorclass=DictCursor)
@app.route('/', methods=['GET'])
def index():
    if "loggedin" in session.keys() and session['loggedin']:
        return redirect('/welcome')
    else:
        session['loggedin']=False
        print("check1")
        return render_template('login1.html')
@app.route('/login',methods=['POST'])
def login():
    if session['loggedin']:
        redirect('/welcome')
    username=request.form['username']
    password=request.form['password']
    if request.form['login_type']=='patient':
        cur.execute("select * from patient where username=%s and password=%s",(username,password))
    else:
        cur.execute("select * from patient where username=%s and password=%s",(username,password))
    data=cur.fetchall()
    if len(data)==0:
        flash('enter valid data')
        return redirect('/')
    #print(jsonify(cur.fetchall()))
    session['data']=data
    session['loggedin']=True
    return redirect('/welcome')
@app.route('/welcome',methods=['GET'])
def welcome():
    return session['data'][0]
@app.route('/report',methods=['GET'])
def test_generate():
    if session['loggedin'] :
        return render_template('creating_symptoms.html')
    return redirect('/')
@app.route('/generate',methods=['POST'])
def generate_result():
    data=prediction.get_diseases(request.form.to_dict())
    print("insert into patient set report='"+data+"' where id="+str(session['data'][0]['id'])+";")
    cur.execute("update patient set report='"+data+"' where username='"+str(session['data'][0]['username'])+"';")
    return render_template('test_report.html',data=eval(data))
@app.route('/register',methods=['POST'])
def register():
    username=request.form['username']
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    age=int(request.form['age'])
    address=request.form['address']
    phone=int(request.form['phone'])
    specialization=request.form['specialization']
    password=request.form['password']
    cur.execute("insert into doctor (username,firstname,lastname,age,address,phone,specialization,password) values(%s,%s,%s,%s,%s,%s,%s,%s);",(username,firstname,lastname,int(age),address,int(phone),specialization,password))
    db_connect.commit()
    return redirect('/')
@app.route('/logout',methods=['GET'])
def logout():
    session['loggedin']=False
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)