from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import funcforweb  # Import your functions
import sqlite3
import hashlib

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend index.html for the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# Endpoint to get moisture changes for a plant
@app.get("/moisture_changes/{plant_id}")
async def get_moisture_changes(plant_id: int):
    try:
        results = funcforweb.get_moisture_changes(plant_id)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get temperature changes for a plant
@app.get("/temperature_changes/{plant_id}")
async def get_temperature_changes(plant_id: int):
    try:
        results = funcforweb.get_temperature_changes(plant_id)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get light changes for a plant
@app.get("/light_changes/{plant_id}")
async def get_light_changes(plant_id: int):
    try:
        results = funcforweb.get_light_changes(plant_id)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Endpoint to get light changes for a plant
@app.get("/humidity_changes/{plant_id}")
async def get_humidity_changes(plant_id: int):
    try:
        results = funcforweb.get_humidity_changes(plant_id)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get plants for an owner
@app.get("/plants_for_owner/{owner_id}")
async def get_plants_for_owner(owner_id: int):
    try:
        results = funcforweb.get_plants_for_owner(owner_id)
        return JSONResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a plant for an owner
@app.post("/add_plant_for_owner")
async def add_plant_for_owner(
    owner_id: int = Form(...),
    plant_name: str = Form(...),
    plant_type: str = Form(...)
):
    try:
        funcforweb.add_plant_for_owner(owner_id, plant_name, plant_type)
        return JSONResponse({"status": "success", "message": "Plant added successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a new owner
@app.post("/add_owner")
async def add_owner(
    owner_name: str = Form(...),
    email: str = Form(...)
):
    try:
        owner_id = funcforweb.add_owner(owner_name, email)
        return JSONResponse({"status": "success", "owner_id": owner_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update contact info for an owner
@app.post("/update_email")
async def update_email(
    owner_id: int = Form(...),
    new_email: str = Form(...)
):
    try:
        funcforweb.update_email(owner_id, new_email)
        return JSONResponse({"status": "success", "message": "Contact info updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to remove a plant
@app.post("/remove_plant")
async def remove_plant(plant_id: int = Form(...)):
    try:
        funcforweb.remove_plant(plant_id)
        return JSONResponse({"status": "success", "message": "Plant removed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#login pages
def verify_login(email, password):
    conn = sqlite3.connect("plant_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT owner_id, password FROM Owners WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        owner_id, hashed_password = user
        if hashlib.sha256(password.encode()).hexdigest() == hashed_password:
            return owner_id
    return None

# Login endpoint
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    owner_id = verify_login(email, password)
    if owner_id:
        return JSONResponse({"status": "success", "owner_id": owner_id})
    else:
        return JSONResponse({"status": "error", "message": "Invalid email or password"}, status_code=401)

# Serve the login page for the root URL
@app.get("/login")
async def serve_login():
    return FileResponse("static/login.html")

# Serve the main page for authenticated users
@app.get("/")
async def serve_main():
    # You can add logic here to check if the user is authenticated
    return FileResponse("static/index.html")

@app.post("/register")
async def register(request: Request):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("plant_management.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Owners (owner_name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        conn.commit()
        return JSONResponse({"status": "success", "message": "Registration successful"})
    except sqlite3.IntegrityError:
        return JSONResponse({"status": "error", "message": "Email already registered"}, status_code=400)
    finally:
        conn.close()

# flaskpart.py
@app.get("/register")
async def serve_register():
    return FileResponse("static/register.html")