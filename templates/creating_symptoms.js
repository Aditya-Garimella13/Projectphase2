var symptoms=['itching', 'nodal_skin_eruptions', 'continuous_sneezing', 'chills',
       'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue',
       'burning_micturition', 'fatigue', 'weight_gain', 'anxiety',
       'cold_hands_and_feets', 'lethargy', 'cough', 'sunken_eyes',
       'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
       'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite',
       'constipation', 'diarrhoea', 'yellow_urine', 'acute_liver_failure',
       'malaise', 'blurred_and_distorted_vision', 'throat_irritation',
       'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion',
       'chest_pain', 'fast_heart_rate', 'pain_during_bowel_movements',
       'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus',
       'neck_pain', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
       'swollen_extremeties', 'excessive_hunger', 'drying_and_tingling_lips',
       'slurred_speech', 'knee_pain', 'hip_joint_pain', 'stiff_neck',
       'swelling_joints', 'movement_stiffness', 'spinning_movements',
       'unsteadiness', 'loss_of_smell', 'passage_of_gases', 'internal_itching',
       'muscle_pain', 'red_spots_over_body', 'dischromic _patches',
       'family_history', 'rusty_sputum', 'visual_disturbances',
       'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
       'stomach_bleeding', 'palpitations', 'painful_walking', 'skin_peeling',
       'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
       'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
function createSymptoms(){
    body=document.getElementById('symptoms-form')
    for(var i=0;i<symptoms.length;i++) {
        heading=document.createElement("label");
        heading.setAttribute("for",symptoms[i]);
        console.log(symptoms[i])
        heading.innerHTML=symptoms[i];
        checkox=document.createElement("input");
        checkox.setAttribute("type","checkbox");
        checkox.name=symptoms[i];
        checkox.value="1";
        checkox.id=symptoms[i]
        body.appendChild(checkox);
        body.appendChild(heading);
        body.appendChild(document.createElement("br")); 
    }
    submit_button=document.createElement('button');
    submit_button.type="submit"
    submit_button.value="generate"
    body.appendChild(submit_button)
}