const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "login.html";
}

const table = document.getElementById("productTable");

window.onload = function () {

    const payload = JSON.parse(atob(token.split(".")[1]));

    document.getElementById("userEmail").innerText = payload.email;
    document.getElementById("userRole").innerText = payload.role;

    loadProducts();
};
async function loadProducts() {

    const response = await fetch(
        "http://127.0.0.1:8002/products",
        {
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    );

    const products = await response.json();

    table.innerHTML = "";

    products.forEach(product => {

        table.innerHTML += `
        <tr>
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.price}</td>

            <td>
                <button class="edit-btn"
                    onclick="editProduct(${product.id})">
                    Edit
                </button>
            </td>

            <td>
                <button class="delete-btn"
                    onclick="deleteProduct(${product.id})">
                    Delete
                </button>
            </td>
        </tr>
        `;
    });

}

function goToAdd() {
    window.location.href = "add_product.html";
}

function editProduct(id) {
    window.location.href = `edit_product.html?id=${id}`;
}

async function deleteProduct(id) {

    if (!confirm("Delete this product?")) {
        return;
    }

    const response = await fetch(
        `http://127.0.0.1:8002/products/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token
            }
        }
    );

    const data = await response.json();

    alert(data.message);

    loadProducts();
}

function logout() {

    localStorage.clear();

    window.location.href = "login.html";

}