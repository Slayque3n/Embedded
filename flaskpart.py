# flaskpart.py
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import funcforweb  # Import your functions
import sqlite3
import ml
import hashlib

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend index.html for the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
    
@app.get("/most_recent_moisture/{plant_id}")
async def get_most_recent_moisture(plant_id: int):
    try:
        value = funcforweb.get_most_recent_change(plant_id, "moisture")
        return JSONResponse({"value": value})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/most_recent_light/{plant_id}")
async def get_most_recent_light(plant_id: int):
    try:
        value = funcforweb.get_most_recent_change(plant_id, "light")
        return JSONResponse({"value": value})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/most_recent_temperature/{plant_id}")
async def get_most_recent_temperature(plant_id: int):
    try:
        value = funcforweb.get_most_recent_change(plant_id, "temperature")
        return JSONResponse({"value": value})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/most_recent_humidity/{plant_id}")
async def get_most_recent_humidity(plant_id: int):
    try:
        value = funcforweb.get_most_recent_change(plant_id, "humidity")
        return JSONResponse({"value": value})
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

# Endpoint to add a new owner
@app.post("/add_owner")
async def add_owner(
    owner_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        owner_id = funcforweb.add_owner(owner_name, email, password)
        return JSONResponse({"status": "success", "owner_id": owner_id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Login endpoint
@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    owner_id = funcforweb.verify_login(email, password)
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

# Serve the register page
@app.get("/register")
async def serve_register():
    return FileResponse("static/register.html")

@app.get("/predict_plant_health/{plant_id}")
async def predict_plant_health(plant_id: int):
    try:
        # Fetch the most recent values for each category
        moisture = funcforweb.get_most_recent_change(plant_id, "moisture")
        temperature = funcforweb.get_most_recent_change(plant_id, "temperature")
        humidity = funcforweb.get_most_recent_change(plant_id, "humidity")
        light = funcforweb.get_most_recent_change(plant_id, "light")

        # Ensure all values are available
        if None in [moisture, temperature, humidity, light]:
            raise HTTPException(status_code=404, detail="Incomplete plant data")
        # Convert values to float (if they are strings)
        moisture = float(moisture)
        temperature = float(temperature)
        humidity = float(humidity)
        light = float(light)

       # Call the ML model to predict plant health
        health_status = ml.predict_health(moisture, temperature, humidity, light)  # Use the ML function
        health_status = str(health_status[0])  # Convert numpy array to str
        return JSONResponse({"health_status": health_status})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

