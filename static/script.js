// Array to store registered plants
let plants = [];
let currentPlantIndex = 0;

// Function to update the plant status
async function updatePlant() {
    const plantId = 1;

    try {
        // Fetch the most recent values for each category
        const moisture = await fetchMostRecentMoisture(plantId);
        const light = await fetchMostRecentLight(plantId);
        const temperature = await fetchMostRecentTemperature(plantId);
        const humidity = await fetchMostRecentHumidity(plantId);

        // Update the UI with the fetched values
        document.getElementById("moisture").textContent = moisture !== null ? `${moisture}%` : "N/A";
        document.getElementById("light").textContent = light !== null ? `${light} lux` : "N/A";
        document.getElementById("temperature").textContent = temperature !== null ? `${temperature}°C` : "N/A";
        document.getElementById("humidity").textContent = humidity !== null ? `${humidity}%` : "N/A";

        //Update the plant icon based on the new values
        //updatePlantIcon();
        await updatePlantHealthIndicator(plantId);
    } catch (error) {
        console.error("Error updating plant status:", error);
        alert("Failed to update plant status. Please try again.");
    }
}

async function fetchMostRecentMoisture(plantId) {
    const response = await fetch(`/most_recent_moisture/${plantId}`);
    const data = await response.json();
    return data.value;
}

async function fetchMostRecentLight(plantId) {
    const response = await fetch(`/most_recent_light/${plantId}`);
    const data = await response.json();
    return data.value;
}

async function fetchMostRecentTemperature(plantId) {
    const response = await fetch(`/most_recent_temperature/${plantId}`);
    const data = await response.json();
    return data.value;
}

async function fetchMostRecentHumidity(plantId) {
    const response = await fetch(`/most_recent_humidity/${plantId}`);
    const data = await response.json();
    return data.value;
}

async function addPlantForOwner(ownerId, plantName) {
    const formData = new FormData();
    formData.append("owner_id", ownerId);
    formData.append("plant_name", plantName);

    const response = await fetch("/add_plant_for_owner", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    console.log(data);
}

async function fetchPlantsForOwner(ownerId) {
    try {
        const response = await fetch(`/plants_for_owner/${ownerId}`);
        const plantIds = await response.json();

        // Fetch plant details for each plant ID
        const plants = [];
        for (const plantId of plantIds) {
            const plantResponse = await fetch(`/plant_details/${plantId}`);
            const plantDetails = await plantResponse.json();
            plants.push(plantDetails);
        }

        // Update the plants array and dropdown
        updatePlantDropdown(plants);
    } catch (error) {
        console.error("Error fetching plants:", error);
    }
}

async function updatePlantHealthIndicator(plantId) {
    try {
        const response = await fetch(`/predict_plant_health/${plantId}`);
        const data = await response.json();

        // Update the UI with the health status
        const healthIndicator = document.getElementById("health-indicator");
        if (healthIndicator) {
            healthIndicator.textContent = `Health Status: ${data.health_status}`;
        } else {
            console.error("Health indicator element not found!");
        }
    } catch (error) {
        console.error("Error updating plant health indicator:", error);
    }
}

// Function to create bubbles for the background animation
function createBubbles() {
    const background = document.getElementById("background");
    for (let i = 0; i < 20; i++) {
        let bubble = document.createElement("div");
        bubble.className = "bubble";
        let size = Math.random() * 50 + 10;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${Math.random() * 100}%`;
        bubble.style.animationDuration = `${Math.random() * 5 + 5}s`;
        background.appendChild(bubble);
    }
}

// Initialize the app
function init() {
    plants = [];

    // Register a default plant
    plants.push({
        name: "Default Plant",
        moisture: 94,
        light: 7,
        temperature: 29,
        humidity: 60
    });
    
    createBubbles();
}

// Run the initialization function when the page loads
init();