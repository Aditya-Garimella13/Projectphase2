from flask import Flask, render_template, request,jsonify,redirect,flash,session
import MySQLdb
from MySQLdb.cursors import DictCursor
import prediction
import specializations_diseases as sd
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
    cur.execute("select * from patient where id="+str(session['data'][0]['id']))
    data=cur.fetchall()
    session['data']=data
    return render_template('Welcome_page.html',data=session['data'][0],report=eval(session['data'][0]['report']))
@app.route('/report',methods=['GET'])
def test_generate():
    symptoms=['itching', 'nodal_skin_eruptions', 'continuous_sneezing', 'chills','joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue','burning_micturition', 'fatigue', 'weight_gain', 'anxiety','cold_hands_and_feets', 'lethargy', 'cough', 'sunken_eyes','breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache','yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite','constipation', 'diarrhoea', 'yellow_urine', 'acute_liver_failure','malaise', 'blurred_and_distorted_vision', 'throat_irritation','redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion','chest_pain', 'fast_heart_rate', 'pain_during_bowel_movements','pain_in_anal_region', 'bloody_stool', 'irritation_in_anus','neck_pain', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails','swollen_extremeties', 'excessive_hunger', 'drying_and_tingling_lips','slurred_speech', 'knee_pain', 'hip_joint_pain', 'stiff_neck','swelling_joints', 'movement_stiffness', 'spinning_movements','unsteadiness', 'loss_of_smell', 'passage_of_gases', 'internal_itching','muscle_pain', 'red_spots_over_body', 'dischromic _patches','family_history', 'rusty_sputum', 'visual_disturbances','receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma','stomach_bleeding', 'palpitations', 'painful_walking', 'skin_peeling','silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails','blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    if session['loggedin'] :
        return render_template('creating_symptoms.html',symptoms=symptoms)
    return redirect('/')
@app.route('/generate',methods=['POST'])
def generate_result():
    data=prediction.get_diseases(request.form.to_dict())
    session['report']=data
    print("insert into patient set report='"+data+"' where id="+str(session['data'][0]['id'])+";")
    cur.execute("update patient set report='"+data+"' where id='"+str(session['data'][0]['id'])+"';")
    db_connect.commit()
    return redirect('/welcome')
@app.route('/recommenddoctor',methods=['GET'])
def recommend_doctor():
    cur.execute("select * from patient where id="+str(session['data'][0]['id']))
    data=cur.fetchall()
    session['data']=data
    doctors_required=sd.get_specialised_doctor(eval(session["data"][0]['report']))
    doctors={}
    for i in list(doctors_required.keys()):
        cur.execute("select * from doctor where specialization='"+doctors_required[i]+"' order by Rating desc limit 2;")
        print(i)    
        doctors[i]=cur.fetchall()
        print(doctors)
    return render_template('doctors_list.html',doctors=doctors)
@app.route('/register',methods=['POST'])
def register():
    username=request.form['username']
    firstname=request.form['firstname']
    lastname=request.form['lastname']
    age=int(request.form['age'])
    address=request.form['address']
    phone=int(request.form['phone'])
    password=request.form['password']
    if request.form['signup_type'] == 'doctor':
        specialization=request.form['specialization']
        cur.execute("insert into doctor (username,firstname,lastname,age,address,phone,specialization,password) values(%s,%s,%s,%s,%s,%s,%s,%s);",(username,firstname,lastname,int(age),address,phone,specialization,password))
    else:
        cur.execute("insert into patient (username,firstname,lastname,age,address,phone,password) values(%s,%s,%s,%s,%s,%s,%s);",(username,firstname,lastname,int(age),address,phone,password))
    db_connect.commit()
    return redirect('/')
@app.route('/ratedoctor',methods=['GET'])
def ratedoctor_get():
    doctorid=request.args['doctorid']
    print(doctorid)
    return render_template('ratedoctor.html',doctorid=doctorid)
@app.route('/ratedoctor',methods=['POST'])
def ratedoctor_post():
    doctorid=request.args['doctorid']
    cur.execute("select rating,nor from doctor where id="+doctorid+";")
    doctor=cur.fetchone()
    print(doctor)
    overall_rating=float(doctor['rating'])*float(doctor['nor'])
    rating=overall_rating+float(request.form['rating'])
    rating=rating/(int(doctor['nor'])+1)
    cur.execute("update doctor set Rating="+str(rating)+"where id="+doctorid+";")
    db_connect.commit()
    return redirect('/recommenddoctor')
@app.route('/logout',methods=['GET'])
def logout():
    session['loggedin']=False
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)