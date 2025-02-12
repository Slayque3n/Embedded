// Array to store registered plants
let plants = [];
let currentPlantIndex = 0;

// Function to update the plant status
function updatePlant() {
    //let moisture = Math.floor(Math.random() * 100);
    let moisture = fetchMoistureChanges(plantId);
    let light = fetchLightChanges(plantId);
    let temperature = fetchTemperatureChanges(plantId);
    let humidity = fetchHumidityChanges(plantId);

    // Update the current plant's data
    plants[currentPlantIndex] = {
        ...plants[currentPlantIndex],
        moisture,
        light,
        temperature,
        humidity
    };

    // Update the UI
    document.getElementById("moisture").textContent = moisture + "%";
    document.getElementById("light").textContent = light + "%";
    document.getElementById("temperature").textContent = temperature + "°C";
    document.getElementById("humidity").textContent = humidity + "%";

    updatePlantIcon();
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
function registerNewPlant() {
    const plantName = prompt("Enter a name for your new plant:");
    if (plantName) {
        // Add a new plant with default values
        plants.push({
            name: plantName,
            moisture: 50,
            light: 50,
            temperature: 25,
            humidity: 50
        });

        // Update the dropdown menu
        updatePlantDropdown();

        // Switch to the new plant
        currentPlantIndex = plants.length - 1;
        switchPlant();
    }
}

// Function to remove the currently selected plant
function removePlant() {
    if (plants.length === 0) {
        alert("No plants to remove!");
        return;
    }

    if (confirm(`Are you sure you want to remove "${plants[currentPlantIndex].name}"?`)) {
        // Remove the current plant
        plants.splice(currentPlantIndex, 1);

        // Update the dropdown menu
        updatePlantDropdown();

        // Switch to the previous plant or reset if no plants are left
        if (plants.length === 0) {
            // No plants left, reset the UI
            currentPlantIndex = -1;
            document.getElementById("moisture").textContent = "N/A";
            document.getElementById("light").textContent = "N/A";
            document.getElementById("temperature").textContent = "N/A";
            document.getElementById("humidity").textContent = "N/A";
            document.getElementById("plant").classList.remove("wilt", "happy", "shake");
        } else {
            // Switch to the previous plant
            currentPlantIndex = Math.max(0, currentPlantIndex - 1);
            switchPlant();
        }
    }
}

// Function to update the dropdown menu with registered plants
function updatePlantDropdown() {
    const select = document.getElementById("plant-select");
    select.innerHTML = ""; // Clear existing options

    plants.forEach((plant, index) => {
        const option = document.createElement("option");
        option.value = index;
        option.textContent = plant.name;
        if (index === currentPlantIndex) {
            option.selected = true;
        }
        select.appendChild(option);
    });
}

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

async function addPlantForOwner(ownerId, plantName, plantType) {
    const formData = new FormData();
    formData.append("owner_id", ownerId);
    formData.append("plant_name", plantName);
    formData.append("plant_type", plantType);

    const response = await fetch("/add_plant_for_owner", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    console.log(data);
}

async function removePlant(plantId) {
    const formData = new FormData();
    formData.append("plant_id", plantId);

    const response = await fetch("/remove_plant", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    console.log(data);
}

// Function to switch between plants
function switchPlant() {
    const select = document.getElementById("plant-select");
    currentPlantIndex = parseInt(select.value);

    // Update the UI with the selected plant's data
    const currentPlant = plants[currentPlantIndex];
    document.getElementById("moisture").textContent = currentPlant.moisture + "%";
    document.getElementById("light").textContent = currentPlant.light + "%";
    document.getElementById("temperature").textContent = currentPlant.temperature + "°C";
    document.getElementById("humidity").textContent = currentPlant.humidity + "%";

    updatePlantIcon();
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
    // Register a default plant
    plants.push({
        name: "Default Plant",
        moisture: 94,
        light: 7,
        temperature: 29,
        humidity: 60
    });

    // Update the dropdown and UI
    updatePlantDropdown();
    switchPlant();
    createBubbles();
}

// Run the initialization function when the page loads
init();