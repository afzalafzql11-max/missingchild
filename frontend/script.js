// Toggle between signup and login forms
function showLogin() {
  document.getElementById("signup_box").style.display = "none";
  document.getElementById("login_box").style.display = "block";
}

function showSignup() {
  document.getElementById("signup_box").style.display = "block";
  document.getElementById("login_box").style.display = "none";
}
