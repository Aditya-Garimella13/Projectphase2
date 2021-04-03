function logintype(){
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
          textbox=document.createElement("input")
          textbox.setAttribute("id","specialization")
          textbox.setAttribute("name","specialization")
          textbox.setAttribute("type", "text")
          textbox.setAttribute("class","input")
          label=document.createElement('label')
          label.setAttribute("for","specialization")
          label.setAttribute("class","label")

          label.innerHTML="specialization"
          group.appendChild(label)
          group.appendChild(textbox)
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


signup_form=document.getElementById("signup-form")
textbox=document.createElement("input")
textbox.setAttribute("id","specialization")
textbox.setAttribute("type", "text")
textbox.setAttribute("class","input")
