async function register(){

    let password =
    document.getElementById("password").value;

    let confirmPassword =
    document.getElementById("confirmPassword").value;

    if(password !== confirmPassword){
        alert("Passwords do not match");
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:8002/register",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                password: password,
                role: document.getElementById("role").value
            })
        }
    );

    const data = await response.json();

    alert(data.message);

    if(response.ok){
        window.location.href = "login.html";
    }
}