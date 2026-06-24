from fastapi import FastAPI
from pydantic import BaseModel
from db import conn, cursor
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MODELS


class Requirement(BaseModel):
    product_id: int
    title: str
    value: str


class RequirementUpdate(BaseModel):
    title: str
    value: str


# HOME

@app.get("/")
def home():
    return {
        "message": "VersionForge Requirement Module"
    }


# ADD REQUIREMENT

@app.post("/requirements")
def add_requirement(req: Requirement):

    query = """
    INSERT INTO requirements
    (product_id, title, value)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            req.product_id,
            req.title,
            req.value
        )
    )

    conn.commit()
    version_response = requests.post(
    f"http://127.0.0.1:8000/versions/create/{req.product_id}")

    version_data = version_response.json()

    version_id = version_data["id"]
    requests.post(
    "http://127.0.0.1:8000/logs/create",
    json={
        "version_id": version_id,
        "requirement_id": cursor.lastrowid,
        "field_name": req.title,
        "old_value": "",
        "new_value": req.value,
        "reason": "Requirement Added",
        "modified_by": "System"
    }
)
    return {
        "message": "Requirement Added",
        "new_value": req.value,
        "version_number": version_data["version_number"]
}


# VIEW REQUIREMENTS

@app.get("/requirements/{product_id}")
def get_requirements(product_id: int):

    query = """
    SELECT *
    FROM requirements
    WHERE product_id = %s
    """

    cursor.execute(query, (product_id,))
    data = cursor.fetchall()

    return data

# UPDATE REQUIREMENT

@app.put("/requirements/{requirement_id}")
def update_requirement(
    requirement_id: int,
    req: RequirementUpdate
):

    # Get old requirement data

    cursor.execute(
        """
        SELECT product_id,
               title,
               value
        FROM requirements
        WHERE requirement_id = %s
        """,
        (requirement_id,)
    )

    old_requirement = cursor.fetchone()

    if not old_requirement:
        return {
            "error": "Requirement not found"
        }

    product_id = old_requirement[0]
    old_title = old_requirement[1]
    old_value = old_requirement[2]

    if old_title == req.title and old_value == req.value:
        return {
        "message": "No changes detected"
        }
    # Update requirement

    cursor.execute(
        """
        UPDATE requirements
        SET title=%s,
            value=%s
        WHERE requirement_id=%s
        """,
        (
            req.title,
            req.value,
            requirement_id
        )
    )

    conn.commit()

    # CREATE VERSION 

    version_response = requests.post(
        f"http://127.0.0.1:8000/versions/create/{product_id}"
    )

    if version_response.status_code != 200:
        return {
            "error": "Version creation failed"
        }

    version_data = version_response.json()

    version_id = version_data["id"]

    # CREATE CHANGE LOG 


    log_response = requests.post(
        "http://127.0.0.1:8000/logs/create",
        json={
            "version_id": version_id,
            "requirement_id": requirement_id,
            "field_name": req.title,
            "old_value": old_value,
            "new_value": req.value,
            "reason": "Requirement Updated",
            "modified_by": "System"
        }
    )

    if log_response.status_code != 200:
        return {
            "error": "Change log creation failed"
        }

    return {
    "message": "Requirement Updated",
    "version_id": version_id,
    "version_number": version_data["version_number"],
    "old_value": old_value,
    "new_value": req.value
}


# DELETE REQUIREMENT

@app.delete("/requirements/{requirement_id}")
def delete_requirement(requirement_id: int):

    query = """
    DELETE FROM requirements
    WHERE requirement_id=%s
    """

    cursor.execute(
        query,
        (requirement_id,)
    )

    conn.commit()

    return {
        "message": "Requirement Deleted"
    }