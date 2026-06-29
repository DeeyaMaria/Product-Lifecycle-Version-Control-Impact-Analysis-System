from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

from database import engine

app = FastAPI()

# JWT Settings
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pydantic Models
# -----------------------------

class Product(BaseModel):
    name: str
    price: float
    user_id: int


class User(BaseModel):
    name: str
    email: str
    password: str
    role: str


class LoginData(BaseModel):
    email: str
    password: str


# -----------------------------
# JWT Function
# -----------------------------

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "Backend Running Successfully"
    }


# -----------------------------
# Get Products
# -----------------------------

@app.get("/products")
def get_products():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT * FROM products")
        )

        products = []

        for row in result:

            products.append({
                "id": row.id,
                "name": row.name,
                "price": float(row.price),
                "user_id": row.user_id
            })

        return products


# -----------------------------
# Add Product
# -----------------------------

@app.post("/products")
def add_product(product: Product):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO products
                (name, price, user_id)
                VALUES
                (:name, :price, :user_id)
            """),
            {
                "name": product.name,
                "price": product.price,
                "user_id": product.user_id
            }
        )

    return {
        "message": "Product Added Successfully"
    }


# -----------------------------
# Update Product
# -----------------------------

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                UPDATE products
                SET
                    name = :name,
                    price = :price,
                    user_id = :user_id
                WHERE id = :id
            """),
            {
                "id": product_id,
                "name": product.name,
                "price": product.price,
                "user_id": product.user_id
            }
        )

        if result.rowcount == 0:

            return {
                "message": "Product Not Found"
            }

    return {
        "message": "Product Updated Successfully"
    }


# -----------------------------
# Delete Product
# -----------------------------

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    with engine.begin() as conn:

        result = conn.execute(
            text("""
                DELETE FROM products
                WHERE id = :id
            """),
            {
                "id": product_id
            }
        )

        if result.rowcount == 0:

            return {
                "message": "Product Not Found"
            }

    return {
        "message": "Product Deleted Successfully"
    }


# -----------------------------
# Register User
# -----------------------------

@app.post("/register")
def register(user: User):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO users
                (name, email, password, role)
                VALUES
                (:name, :email, :password, :role)
            """),
            {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "role": user.role
            }
        )

    return {
        "message": "User Registered Successfully"
    }


# -----------------------------
# Login User + JWT
# -----------------------------

@app.post("/login")
def login(user: LoginData):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT * FROM users
                WHERE email = :email
                AND password = :password
            """),
            {
                "email": user.email,
                "password": user.password
            }
        )

        db_user = result.fetchone()

        if db_user:

            token = create_access_token(
                {
                    "email": db_user.email,
                    "role": db_user.role
                }
            )

            return {
                "access_token": token,
                "token_type": "bearer",
                "role": db_user.role,
                "email": db_user.email,
                "name": db_user.name
}

        return {
            "message": "Invalid Email or Password"
        }