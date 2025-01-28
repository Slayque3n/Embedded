<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ owner_name }}'s Plants</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>{{ owner_name }}'s Plants</h1>
        <ul id="plant-list">
            {% for plant in plants %}
                <li>Plant ID: {{ plant[0] }}, Description: {{ plant[1] }}</li>
            {% endfor %}
        </ul>

        <h2>Register a New Plant</h2>
        <form id="register-plant-form">
            <input type="hidden" name="owner_name" value="{{ owner_name }}">
            <label for="change_description">Plant Description:</label>
            <input type="text" id="change_description" name="change_description" required>
            <button type="submit">Register Plant</button>
        </form>
    </div>
    <script src="/static/main.js"></script>
</body>
</html>
