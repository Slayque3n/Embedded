from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Connect to the database
def connect_db():
    return sqlite3.connect("plant_management.db")

@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.post("/add_user", response_class=JSONResponse)
async def add_user(owner_name: str = Form(...), contact_info: str = Form(...)):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Owners (owner_name, contact_info) VALUES (?, ?)", (owner_name, contact_info))
    conn.commit()
    conn.close()
    return {"message": "User added successfully"}

@app.get("/user_plants/{owner_name}", response_class=HTMLResponse)
async def user_plants(request: Request, owner_name: str):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT owner_id FROM Owners WHERE owner_name = ?", (owner_name,))
    owner = cursor.fetchone()

    if not owner:
        return "Owner not found", 404

    owner_id = owner[0]
    cursor.execute("""
        SELECT c.plant_id, c.change_description 
        FROM Changes c
        JOIN Ownership o ON c.plant_id = o.plant_id
        WHERE o.owner_id = ?
    """, (owner_id,))
    plants = cursor.fetchall()
    conn.close()

    return templates.TemplateResponse("user_plants.html", {"request": request, "owner_name": owner_name, "plants": plants})

@app.post("/register_plant", response_class=JSONResponse)
async def register_plant(owner_name: str = Form(...), change_description: str = Form(...)):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT owner_id FROM Owners WHERE owner_name = ?", (owner_name,))
    owner = cursor.fetchone()

    if not owner:
        return {"error": "Owner not found"}, 404

    owner_id = owner[0]
    cursor.execute("INSERT INTO Changes (plant_id, change_description) VALUES (NULL, ?)", (change_description,))
    conn.commit()

    cursor.execute("SELECT plant_id FROM Changes WHERE change_description = ? ORDER BY time DESC LIMIT 1", (change_description,))
    plant_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO Ownership (owner_id, plant_id) VALUES (?, ?)", (owner_id, plant_id))
    conn.commit()
    conn.close()

    return {"message": "Plant registered successfully"}
