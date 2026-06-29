async function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email === "" || password === "") {
        alert("Fill all fields");
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:8002/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }
    );

    const data = await response.json();

    if (data.access_token) {

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("email", data.email);
        localStorage.setItem("role", data.role);
        localStorage.setItem("name", data.name);

        alert("Login Successful");

        window.location.href = "main.html";
    }
    else {
        alert(data.message);
    }
}