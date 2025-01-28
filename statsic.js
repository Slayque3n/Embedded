// Handle adding a new user
document.addEventListener("DOMContentLoaded", () => {
    const addUserForm = document.getElementById("add-user-form");
    const registerPlantForm = document.getElementById("register-plant-form");

    if (addUserForm) {
        addUserForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(addUserForm);
            const response = await fetch("/add_user", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                window.location.href = `/user_plants/${formData.get("owner_name")}`;
            } else {
                alert("Error adding user.");
            }
        });
    }

    if (registerPlantForm) {
        registerPlantForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(registerPlantForm);
            const response = await fetch("/register_plant", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();

            if (response.ok) {
                alert(data.message);
                location.reload();
            } else {
                alert("Error registering plant.");
            }
        });
    }
});
