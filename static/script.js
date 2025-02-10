function updatePlant() {
    let moisture = Math.floor(Math.random() * 100);
    let light = Math.floor(Math.random() * 100);
    let temperature = Math.floor(Math.random() * 40);
    let happiness = Math.floor(Math.random() * 100);
    
    document.getElementById("moisture").textContent = moisture + "%";
    document.getElementById("light").textContent = light + "%";
    document.getElementById("temperature").textContent = temperature + "°C";
    document.getElementById("happiness").textContent = happiness + "%";
    
    let plant = document.getElementById("plant");
    
    // Wilt if moisture < 30% or light < 20%
    if (moisture < 30 || light < 20) {
        plant.classList.add("wilt");
        plant.classList.remove("happy", "shake");
    } else {
        plant.classList.remove("wilt");
    }
    
    // Glow and bounce if happiness > 80%
    if (happiness > 80) {
        plant.classList.add("happy");
        plant.classList.remove("wilt", "shake");
    } else {
        plant.classList.remove("happy");
    }
    
    // Shake if temperature > 35°C
    if (temperature > 35) {
        plant.classList.add("shake");
    } else {
        plant.classList.remove("shake");
    }
}

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

createBubbles();