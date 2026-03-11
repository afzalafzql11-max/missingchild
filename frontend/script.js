const API="https://image-dehazer-x8aa.onrender.com"

let user_id=null


async function signup(){

let email=document.getElementById("signup_email").value
let password=document.getElementById("signup_pass").value

await fetch(API+"/signup",{

method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email,password})

})

alert("Account created")

}


async function login(){

let email=document.getElementById("login_email").value
let password=document.getElementById("login_pass").value

let res=await fetch(API+"/login",{

method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email,password})

})

let data=await res.json()

if(data.status==="success"){

user_id=data.user_id

document.getElementById("auth").style.display="none"
document.getElementById("dashboard").style.display="block"

}else{

alert("Invalid Login")

}

}


function previewImage(){

let file=document.getElementById("image").files[0]

let reader=new FileReader()

reader.onload=function(){

let img=document.getElementById("preview")
img.src=reader.result
img.style.display="block"

}

reader.readAsDataURL(file)

}


async function upload(){

let file=document.getElementById("image").files[0]

let form=new FormData()

form.append("user_id",user_id)
form.append("image",file)

let res=await fetch(API+"/dehaze",{

method:"POST",
body:form

})

let blob=await res.blob()

let url=URL.createObjectURL(blob)

let a=document.createElement("a")

a.href=url
a.download="dehazed.jpg"

a.click()

}


async function loadHistory(){

let res=await fetch(API+"/history/"+user_id)

let data=await res.json()

let html="<h3>Your History</h3>"

data.forEach(img=>{

html+=`

<div class="history-card">

<a href="${API}/download?path=${img}" target="_blank">

Download Image

</a>

</div>

`

})

document.getElementById("history").innerHTML=html

}
