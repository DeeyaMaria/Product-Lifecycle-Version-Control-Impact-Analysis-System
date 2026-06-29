async function addProduct() {

    const name =
    document.getElementById("name").value;

    const price =
    document.getElementById("price").value;

    if(name === "" || price === ""){
        alert("please fill all fields");
        return;
    }

    const response =
    await fetch(
        "http://127.0.0.1:8002/products",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                price: Number(price),
                user_id: 1
            })
        }
    );

    const data =
    await response.json();

    alert(data.message);

    window.location.href =
    "dashboard.html";
}