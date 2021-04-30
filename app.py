from flask import Flask, render_template, request,jsonify,redirect,flash,session
import MySQLdb
from MySQLdb import IntegrityError
import json
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
errors={}
errors['1062']="Entry already exists"
def is_json(myjson):

    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
def create_update_query(formdata):
    print(formdata)
    # query=""
    # if "username" in formdata:
    #     query=query+"username="+formdata['username']+"," 
    # if "firstname" in formdata:
    #     query=query+"firstname="+formdata['firstname']+","
    # if "lastname" in formdata:
    #     query=query+"lastname="+formdata['lastname']+","
    # if "age" in formdata:
    #     query=query+"age="+formdata['age']+","
    # if "address" in formdata:
    #     query=query+"address="+formdata['address']+","
    # if "phone" in formdata:
    #     query=query+""

    query=', '.join("{!s}={!r}".format(key,val) for (key,val) in formdata.items() if val!='')
    print("query is "+query)
    return query
    
@app.route('/', methods=['GET'])
def index():
    if "loggedin" in session.keys() and session['loggedin']:
        return redirect('/welcome_'+session['login_type'])
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
        print("checking the login")
        cur.execute("select * from doctor where username=%s and password=%s",(username,password))
    data=cur.fetchall()
    if len(data)==0:
        print("wrong data")
        flash('enter valid data')
        return redirect('/')
    #print(jsonify(cur.fetchall()))
    session['login_type']=request.form['login_type']
    session['data']=data
    session['loggedin']=True
    if session['login_type']=='patient':
        return redirect('/welcome_patient')
    else:
        return redirect("/welcome_doctor")
@app.route('/welcome_patient',methods=['GET'])
def welcome():
    cur.execute("select * from patient where id="+str(session['data'][0]['id']))
    data=cur.fetchall()
    session['data']=data
    report=None
    print(type(session['data'][0]['report']))
    print(session['data'][0]['report'] is not None)
    if session['data'][0]['report'] is not None and is_json(session['data'][0]['report']):
        report=eval(session['data'][0]['report'])
    return render_template('Welcome_page_patient.html',data=session['data'][0],report=report)
@app.route('/welcome_doctor',methods=['GET'])
def welcome_doctor():
    return "Hello doctor"
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
    return redirect('/welcome_patient')
@app.route('/recommenddoctor',methods=['GET'])
def recommend_doctor():
    cur.execute("select * from patient where id="+str(session['data'][0]['id']))
    data=cur.fetchall()
    session['data']=data
    if is_json(session["data"][0]['report']):
        doctors_required=sd.get_specialised_doctor(eval(session["data"][0]['report']))
        doctors={}
        for i in list(doctors_required.keys()):
            cur.execute("select * from doctor where specialization='"+doctors_required[i]+"' order by Rating desc limit 2;")
            print(i)    
            doctors[i]=cur.fetchall()
            print(doctors)
        return render_template('doctors_list.html',doctors=doctors)
    else:
        return "Generate report to find doctors"
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
@app.route('/edit',methods=['GET'])
def get_edit():
    return render_template('edit_profile.html',data=session["data"][0])
@app.route('/edit',methods=['POST'])
def post_edit():
    insert_query=create_update_query(request.form)
    if insert_query=="":
        return redirect('/welcome_'+session['login_type'])
    else:
        if session['login_type']=='patient':
            cur.execute("update patient set "+insert_query+" where id="+str(session["data"][0]['id']))
        else:
            cur.execute("update doctor set "+insert_query+" where id="+str(session["data"][0]['id']))
    db_connect.commit()
    flash('Updated Profile')
    return redirect('/welcome_'+session['login_type'])
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
    cur.execute("update doctor set nor="+str(int(doctor['nor'])+1)+" where id="+doctorid+";")
    db_connect.commit()
    return redirect('/recommenddoctor')
@app.route('/book_appointment',methods=['GET'])
def book_appointment():
    doctorid =request.args.get('doctorid')
    disease=request.args.get('disease')
    print(disease)
    data={}
    data['disease']=disease
    data['doctorid']=doctorid
    return render_template('appointment_booking.html',data=data)
@app.route('/book_appointment',methods=['POST'])
def post_book_appointment():
    date=request.form.get('date')
    ses=request.form.get('session')
    doctorid=request.args.get('doctorid')
    disease=request.form.get('disease')
    print('insert into Appointments values('+str(session['data'][0]['id'])+","+str(doctorid)+',"'+ses+'","'+disease+'","'+date+'");')
    try:
        cur.execute('insert into Appointments values('+str(session['data'][0]['id'])+","+str(doctorid)+',"'+ses+'","'+disease+'","'+date+'");')
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(errors[str(e.args[0])])
    db_connect.commit()
    return redirect('/recommenddoctor')
@app.route('/appointments',methods=['GET'])
def get_appointments():
    if session['login_type']=='patient':
        cur.execute("select * from Appointments join doctor on doctor.id=Appointments.doctor_id where Appointments.patient_id="+str(session['data'][0]['id'])+";")
    else:
        cur.execute("select * from Appointments where doctor_id="+str(session['data'][0]['id'])+";")
    appointments = cur.fetchall()
    appointments=list(appointments)
    print(appointments)
    return render_template('appointments.html',login_type=session['login_type'],appointments=appointments)
@app.route('/logout',methods=['GET'])
def logout():
    session['loggedin']=False
    return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)