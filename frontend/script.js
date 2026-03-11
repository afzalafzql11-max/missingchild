const API = "https://image1dehazer.onrender.com"

async function uploadImage(){

const file = document.getElementById("image").files[0]

if(!file){
alert("Please select image")
return
}

const formData = new FormData()
formData.append("image", file)

const res = await fetch(API + "/dehaze",{

method:"POST",
body:formData

})

const blob = await res.blob()

const url = window.URL.createObjectURL(blob)

const a = document.createElement("a")

a.href = url
a.download = "dehazed_image.png"
a.click()

}
