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

// Function to update the plant icon based on conditions
function updatePlantIcon() {
    let plant = document.getElementById("plant");
    let currentPlant = plants[currentPlantIndex];

    // Wilt if moisture < 30% or light < 20%
    if (currentPlant.moisture < 30 || currentPlant.light < 20) {
        plant.classList.add("wilt");
        plant.classList.remove("happy", "shake");
    } else {
        plant.classList.remove("wilt");
    }

    // Glow and bounce if humidity > 80%
    if (currentPlant.humidity > 80) {
        plant.classList.add("happy");
        plant.classList.remove("wilt", "shake");
    } else {
        plant.classList.remove("happy");
    }

    // Shake if temperature > 35°C
    if (currentPlant.temperature > 35) {
        plant.classList.add("shake");
    } else {
        plant.classList.remove("shake");
    }
}

// Function to register a new plant
// function registerNewPlant() {
//     const plantName = prompt("Enter a name for your new plant:");
//     if (plantName) {
//         // Assuming the owner ID is known (e.g., stored in a variable or retrieved from the session)
//         const ownerId = 1; // Replace this with the actual owner ID (e.g., from login)

//         // Call the backend to add the plant
//         addPlantForOwner(ownerId, plantName)
//             .then(() => {
//                 // Refresh the plant list after adding a new plant
//                 fetchPlantsForOwner(ownerId);
//             })
//             .catch(error => {
//                 console.error("Error adding plant:", error);
//                 alert("Failed to add the plant. Please try again.");
//             });
//     }
// }

// Function to remove the currently selected plant
// async function removePlant() {
//     const select = document.getElementById("plant-select");
//     const plantId = select.value; // Get the selected plant's ID

//     if (!plantId) {
//         alert("No plant selected!");
//         return;
//     }

//     if (confirm(`Are you sure you want to remove this plant?`)) {
//         try {
//             const response = await fetch("/remove_plant", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({ plant_id: parseInt(plantId) }) // Ensure plant_id is sent as an integer
//             });

//             if (response.ok) {
//                 alert("Plant removed successfully!");
//                 // Refresh the plant list after removal
//                 const ownerId = 1; // Replace with the actual owner ID
//                 fetchPlantsForOwner(ownerId);
//             } else {
//                 const errorData = await response.json();
//                 alert(`Failed to remove plant: ${errorData.detail}`);
//             }
//         } catch (error) {
//             console.error("Error removing plant:", error);
//             alert("Failed to remove plant. Please try again.");
//         }
//     }
// }

// Function to update the dropdown menu with registered plants
// function updatePlantDropdown(plants) {
//     const select = document.getElementById("plant-select");
//     select.innerHTML = ""; // Clear existing options

//     plants.forEach((plant, index) => {
//         const option = document.createElement("option");
//         option.value = plant.plant_id; // Use plant_id as the value
//         option.textContent = plant.plant_name; // Use plant_name as the display text
//         select.appendChild(option);
//     });

//     // Switch to the newly added plant
//     if (plants.length > 0) {
//         currentPlantIndex = plants.length - 1;
//         switchPlant();
//     }
// }

// function switchPlant() {
//     const select = document.getElementById("plant-select");
//     currentPlantIndex = parseInt(select.value);
//     // Update the UI with the selected plant's data
//     const currentPlant = plants[currentPlantIndex];
//     document.getElementById("moisture").textContent = currentPlant.moisture + "%";
//     document.getElementById("light").textContent = currentPlant.light + "%";
//     document.getElementById("temperature").textContent = currentPlant.temperature + "°C";
//     document.getElementById("humidity").textContent = currentPlant.humidity + "%";
//     updatePlantIcon();
// }

async function fetchMoistureChanges(plantId) {
    const response = await fetch(`/moisture_changes/${plantId}`);
    const data = await response.json();
    console.log(data);
}

async function fetchTemperatureChanges(plantId) {
    const response = await fetch(`/temperature_changes/${plantId}`);
    const data = await response.json();
    console.log(data);
}

async function fetchLightChanges(plantId) {
    const response = await fetch(`/light_changes/${plantId}`);
    const data = await response.json();
    console.log(data);
}

async function fetchHumidityChanges(plantId) {
    const response = await fetch(`/humidity_changes/${plantId}`);
    const data = await response.json();
    console.log(data);
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

// async function removePlant() {
//     const select = document.getElementById("plant-select");
//     const plantId = select.value; // Get the selected plant's ID

//     if (!plantId) {
//         alert("No plant selected!");
//         return;
//     }

//     if (confirm(`Are you sure you want to remove this plant?`)) {
//         try {
//             const response = await fetch("/remove_plant", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json" // Ensure the correct content type
//                 },
//                 body: JSON.stringify({ plant_id: parseInt(plantId) }) // Send plant_id as an integer in JSON format
//             });

//             if (response.ok) {
//                 alert("Plant removed successfully!");
//                 // Refresh the plant list after removal
//                 const ownerId = 1; // Replace with the actual owner ID
//                 fetchPlantsForOwner(ownerId);
//             } else {
//                 const errorData = await response.json();
//                 alert(`Failed to remove plant: ${errorData.detail}`);
//             }
//         } catch (error) {
//             console.error("Error removing plant:", error);
//             alert("Failed to remove plant. Please try again.");
//         }
//     }
// }

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

    // Update the dropdown and UI
    //updatePlantDropdown(plants);
    // switchPlant();
    createBubbles();
}

// Run the initialization function when the page loads
init();