function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let errorMsg = document.getElementById("errorMsg");

    // Dummy credentials
    if (username === "admin" && password === "1234") {
        alert("Login Successful!");
       window.location.href = "personalinfo.html";
    } else {
        errorMsg.innerText = "Invalid Username or Password";
    }
}

function submitPersona() {

    let freeTime = document.getElementById("freeTime").value;
    let hobby = document.getElementById("hobby").value;
    let happyAction = document.getElementById("happyAction").value;
    let sadAction = document.getElementById("sadAction").value;
    let personality = document.getElementById("personality").value;

    if (freeTime === "" || hobby === "" || happyAction === "" || sadAction === "" || personality === "") {
        document.getElementById("message").innerText = "Please fill all details!";
    } else {

        // Store data in localStorage
        localStorage.setItem("freeTime", freeTime);
        localStorage.setItem("hobby", hobby);
        localStorage.setItem("happyAction", happyAction);
        localStorage.setItem("sadAction", sadAction);
        localStorage.setItem("personality", personality);

        alert("Persona Data Saved Successfully!");
        window.location.href = "personalinfo.html";
    }
}
