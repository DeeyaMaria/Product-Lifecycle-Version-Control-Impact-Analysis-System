const params = new URLSearchParams(window.location.search);

const id = Number(params.get("id"));

loadProduct();

async function loadProduct() {

    const response =
    await fetch("http://127.0.0.1:8002/products");

    const products =
    await response.json();

    const product =
    products.find(p => p.id === id);

    document.getElementById("name").value =
    product.name;

    document.getElementById("price").value =
    product.price;
}

async function updateProduct() {

    const name =
    document.getElementById("name").value;

    const price =
    document.getElementById("price").value;

    if(name === "" || price ===""){
        alert("please fill all fields");
        return;
    }

    const response =
    await fetch(
        `http://127.0.0.1:8002/products/${id}`,
        {
            method: "PUT",

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