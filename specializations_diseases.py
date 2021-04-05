Audiologist=['(vertigo) Paroymsal  Positional Vertigo']
Aids=['Aids']
Dermatologist=['Acne','Fungal infection','Impetigo','Psoriasis']
Gastroenterologist=["Alcoholic hepatitis", "Chronic cholestasis", "GERD", "Gastroenteritis", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E", "Jaundice", "Peptic ulcer diseae", "hepatitis A"]
Allergist=["Allergy", "Bronchial Asthma", "Drug Reaction"]
Rheumatologists=["Arthritis", "Osteoarthristis"]
Orthopedic=['Cervical spondylosis']
General_physician=["Chicken pox", "Common Cold", "Dimorphic hemmorhoids(piles)"]
Infectious_diseases_specialist=['Dengue','Malaria','Typhoid']
Endocrinologists=["Diabetes", "Hyperthyroidism", "Hypoglycemia", "Hypothyroidism"]
Cardiologist=["Heart attack", "Hypertension"]
Neurologist=['Migrane', 'Paralysis (brain hemorrhage)']
Pulmonologist=['Pneumonia','Tuberculosis']
Urologist=['Urinary tract infection']
Phlebology=['Varicose veins']
specializations=[Audiologist,Aids,Dermatologist,Gastroenterologist,Allergist,Rheumatologists,Orthopedic,General_physician,Infectious_diseases_specialist,Endocrinologists,Cardiologist,Neurologist,Pulmonologist,Urologist,Phlebology]
specializations_names=["Audiologist","Aids","Dermatologist","Gastroenterologist","Allergist","Rheumatologists","Orthopedic","General physician","Infectious diseases specialist","Endocrinologists","Cardiologist","Neurologist","Pulmonologist","Urologist","Phlebology"]
def get_specialised_doctor(report):
    return_values={}
    diseases=list(report.keys())[:2]
    print("diseases are :")
    print(diseases)
    for i in diseases:
        for j in range(len(specializations)):
            if i in specializations[j]:
                print(specializations_names[j])
                return_values[i]=specializations_names[j]
    return return_values