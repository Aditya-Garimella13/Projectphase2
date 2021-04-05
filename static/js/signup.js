function logintype(){
  specializations=['Audiologist','Aids','Dermatologist','Gastroenterologist','Allergist','Rheumatologists','Orthopedic','General physician','Infectious diseases specialist','Endocrinologists','Cardiologist',
  'Neurologist','Pulmonologist','Urologist','Phlebology']
  var radios=document.getElementsByName('signup_type')
  for(var i=0;i<radios.length;i++) {
    if(radios[i].checked){
      if(radios[i].value=="doctor") {
        if (document.getElementById('specialization') == null){
          signup_form=document.getElementById("signup-form")
          group=document.createElement("div")
          group.setAttribute("class","group" )
          group.setAttribute("id","specializationgroup")
          signup_form.appendChild(group)
          textbox=document.createElement("select")
          textbox.setAttribute("id","specialization")
          textbox.setAttribute("name","specialization")
          textbox.setAttribute("class","input")
          // textbox.setAttribute("type", "text")
          // textbox.setAttribute("class","input")
          label=document.createElement('label')
          label.setAttribute("for","specialization")
          label.setAttribute("class","label")

          label.innerHTML="specialization"
          group.appendChild(label)
          group.appendChild(textbox)
          createlist(specializations);
          document.getElementById('signup').before(group)
        }
      }
      else if(radios[i].value=="patient"){
        if(document.getElementById("specialization")==null) {

        }
        else {
          console.log("check")
          document.getElementById('specializationgroup').remove()
        }
      }
    }
  }
}
function createlist(s){
  specialization=document.getElementById('specialization')
  for(var i=0;i<s.length;i++) {
    opt=document.createElement('option');
    opt.setAttribute('value',s[i])
    opt.setAttribute('style','color:blue')
    opt.innerHTML=s[i]
    specialization.appendChild(opt)
  }
}

signup_form=document.getElementById("signup-form")
textbox=document.createElement("input")
textbox.setAttribute("id","specialization")
textbox.setAttribute("type", "text")
textbox.setAttribute("class","input")
