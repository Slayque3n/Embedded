// register.js
document.getElementById("register-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to the login page
            window.location.href = "/login";
        } else {
            // Show error message
            document.getElementById("error-message").textContent = data.message;
            document.getElementById("error-message").style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("error-message").textContent = "An error occurred. Please try again.";
        document.getElementById("error-message").style.display = "block";
    }
});