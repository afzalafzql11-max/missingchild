const API = "https://dehazer1.onrender.com";

let user_id = null;

// ---------- UI FUNCTIONS ----------
function showLogin() {
  document.getElementById("signup_box").style.display = "none";
  document.getElementById("login_box").style.display = "block";
}

function showSignup() {
  document.getElementById("signup_box").style.display = "block";
  document.getElementById("login_box").style.display = "none";
}

// ---------- SIGNUP ----------
async function signup() {
  let email = document.getElementById("signup_email").value.trim();
  let password = document.getElementById("signup_pass").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    let res = await fetch(API + "/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    let data = await res.json();

    if (data.status === "success") {
      alert("Signup successful! Please login.");
      showLogin();
    } else {
      alert(data.message || "Signup failed");
    }
  } catch (err) {
    alert("Error connecting to server");
    console.error(err);
  }
}

// ---------- LOGIN ----------
async function login() {
  let email = document.getElementById("login_email").value.trim();
  let password = document.getElementById("login_pass").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    let res = await fetch(API + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    let data = await res.json();

    if (data.status === "success") {
      user_id = data.user_id;
      document.getElementById("auth").style.display = "none";
      document.getElementById("dashboard").style.display = "block";
    } else {
      alert(data.message || "Invalid login credentials");
    }
  } catch (err) {
    alert("Error connecting to server");
    console.error(err);
  }
}

// ---------- UPLOAD IMAGE ----------
async function upload() {
  let file = document.getElementById("image").files[0];

  if (!file) {
    alert("Please select an image to upload");
    return;
  }

  let form = new FormData();
  form.append("user_id", user_id);
  form.append("image", file);

  try {
    let res = await fetch(API + "/dehaze", { method: "POST", body: form });

    if (!res.ok) {
      alert("Failed to dehaze image");
      return;
    }

    let blob = await res.blob();
    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = "dehazed.jpg";
    a.click();

    alert("Image dehazed successfully!");
  } catch (err) {
    alert("Error uploading image");
    console.error(err);
  }
}

// ---------- LOAD HISTORY ----------
async function loadHistory() {
  try {
    let res = await fetch(API + "/history/" + user_id);
    let data = await res.json();

    if (!data.length) {
      document.getElementById("history").innerHTML = "<p>No images yet</p>";
      return;
    }

    let html = "<h3>Your Images</h3>";

    data.forEach(img => {
      html += `<br>
      <a href="${API}/download?path=${encodeURIComponent(img)}" target="_blank">
        Download Image
      </a>`;
    });

    document.getElementById("history").innerHTML = html;
  } catch (err) {
    alert("Error loading history");
    console.error(err);
  }
}
