from joblib import load
import numpy as np
import json
import operator
model = load('classification.joblib')
classes=list(model.classes_)
def get_diseases(data):
    symptoms=['itching', 'nodal_skin_eruptions', 'continuous_sneezing', 'chills','joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue','burning_micturition', 'fatigue', 'weight_gain', 'anxiety','cold_hands_and_feets', 'lethargy', 'cough', 'sunken_eyes','breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache','yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite','constipation', 'diarrhoea', 'yellow_urine', 'acute_liver_failure','malaise', 'blurred_and_distorted_vision', 'throat_irritation','redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion','chest_pain', 'fast_heart_rate', 'pain_during_bowel_movements','pain_in_anal_region', 'bloody_stool', 'irritation_in_anus','neck_pain', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails','swollen_extremeties', 'excessive_hunger', 'drying_and_tingling_lips','slurred_speech', 'knee_pain', 'hip_joint_pain', 'stiff_neck','swelling_joints', 'movement_stiffness', 'spinning_movements','unsteadiness', 'loss_of_smell', 'passage_of_gases', 'internal_itching','muscle_pain', 'red_spots_over_body', 'dischromic _patches','family_history', 'rusty_sputum', 'visual_disturbances','receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma','stomach_bleeding', 'palpitations', 'painful_walking', 'skin_peeling','silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails','blister', 'red_sore_around_nose', 'yellow_crust_ooze']
    values=np.zeros(79).tolist()
    dictionary_of_symptoms=dict(zip(symptoms,values))
    for i in dictionary_of_symptoms.keys():
        if i in data.keys():
            dictionary_of_symptoms[i]=1
    a=list(dictionary_of_symptoms.values())
    print(a)
    predictions=model.predict_proba([a])
    predictions_list=predictions[0]
    res = dict(zip(classes, predictions_list))
    for i in res.keys():
        res[i]=int(res[i]*100)
    res = {k:v for k,v in res.items() if v >0}
    res = dict(sorted(res.items(), key=lambda x: x[1], reverse=True))
    res=json.dumps(res)
    print(len(res))
    return res


