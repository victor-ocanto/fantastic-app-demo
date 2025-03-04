from flask import Flask, request, jsonify, render_template_string, redirect
import os, psycopg2, requests
from psycopg2 import OperationalError, errorcodes

app = Flask(__name__)

# Aurora Database Configuration from Environment Variables
DB_HOST = os.getenv("DB_HOST", "your-cluster.cluster-xxxxxxxxxx.region.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DB_PORT = os.getenv("DB_PORT", "5432")  

# Establish Database Connection with Error Handling
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except OperationalError as e:
        error_msg = f"Database connection error: {e}"
        app.logger.error(error_msg)
        raise Exception(error_msg)  # Raise the error for further handling
    except Exception as e:
        error_msg = f"Unknown error while connecting to the database: {e}"
        app.logger.error(error_msg)
        raise Exception(error_msg)

@app.route('/health')
def health():
    return jsonify({"message": "Fantastic App is running!"}), 200

@app.route('/readiness')
def readiness():
    return jsonify({"message": "Fantastic App is running!"}), 200

@app.route('/')
def home():
    # Get data from /read endpoint
    try:
        # Make a request to the /read route to fetch the users data
        response = requests.get("http://127.0.0.1:5000/read")
        if response.status_code == 200:
            users = response.json()
        else:
            users = {"error": "Unable to fetch users data"}

        # Render the home page with users data and the form
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Users List</title>
        </head>
        <body>
        <h1>Users List</h1>
        <ul>
        {% for user in users %}
            <li>{{ user[1] }} {{ user[2] }} ({{ user[3] }})</li>
        {% endfor %}
        </ul>

        <h2>Add a New User</h2>
        <form action="/add" method="POST">
            <label for="name">First Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            <label for="lastname">Last Name:</label>
            <input type="text" id="lastname" name="lastname" required><br><br>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>
            <button type="submit">Add User</button>
        </form>
        </body>
        </html>
        """, users=users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get("name")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    
    if not name or not lastname or not email:
        return jsonify({"error": "All fields are required!"}), 400

    try:
        # Insert the new user into the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, lastname, email) VALUES (%s, %s, %s)",
            (name, lastname, email)
        )
        conn.commit()

        cur.close()
        conn.close()

        # Redirect back to the homepage to show the updated list
        return redirect('/')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/read', methods=['GET'])
def read_data():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
