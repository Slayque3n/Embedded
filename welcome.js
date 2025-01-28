<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Plant Manager</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Welcome to Plant Manager!</h1>
        <form id="add-user-form">
            <h2>Add a New User</h2>
            <label for="owner_name">Your Name:</label>
            <input type="text" id="owner_name" name="owner_name" required>
            
            <label for="contact_info">Your Contact Info:</label>
            <input type="text" id="contact_info" name="contact_info" required>
            
            <button type="submit">Add User</button>
        </form>
    </div>
    <script src="/static/main.js"></script>
</body>
</html>
