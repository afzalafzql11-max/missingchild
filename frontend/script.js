const API = "https://dehazer-sf8p.onrender.com"

let current_user=""

function signup(){

fetch(API+"/signup",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:su_user.value,
password:su_pass.value
})
}).then(r=>r.json()).then(d=>{
alert("Signup success")
})

}

function login(){

fetch(API+"/login",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:li_user.value,
password:li_pass.value
})
}).then(r=>r.json()).then(d=>{

if(d.status=="success"){

current_user=li_user.value

auth.style.display="none"
dashboard.style.display="block"

load_history()

}else{

alert("Login failed")

}

})

}

function upload(){

let file=image.files[0]

let form=new FormData()
form.append("image",file)
form.append("username",current_user)

fetch(API+"/upload",{method:"POST",body:form})
.then(r=>r.blob())
.then(b=>{

result.src=URL.createObjectURL(b)

load_history()

})

}

function load_history(){

fetch(API+"/history/"+current_user)
.then(r=>r.json())
.then(data=>{

history.innerHTML=""

data.forEach(p=>{

history.innerHTML+=`<br>
<a href="${API}/download?path=${p}" target="_blank">
Download Image
</a>`

})

})

}
