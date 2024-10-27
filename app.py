from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import hashlib
import os

app = Flask(__name__)

# Ścieżka do pliku bazy danych
DATABASE = 'users.db'

app.secret_key = "your_secret_key"  # Set a unique and secure secret key here


def initialize_database():
    # Sprawdzamy, czy plik bazy danych już istnieje
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Tworzenie tabeli użytkowników
        cursor.execute('''CREATE TABLE users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            password TEXT,
                            role TEXT)''')
        print("Table 'users' created.")
        
        # Wstawianie przykładowych użytkowników
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        cursor.execute("INSERT INTO users (username, password) VALUES ('guest', 'guest123')")
        
        # Zatwierdzenie i zamknięcie połączenia
        conn.commit()
        conn.close()
        print("Database initialized with sample data.")
    else:
        print("Database already exists. Skipping initialization.")

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    result = None  # Initialize result variable to store search results
    if request.method == 'POST':
        username = request.form.get('username')
        
        # SQL injection point - podatne zapytanie
        query = f"SELECT * FROM users WHERE username = '{username}'"
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute(query)
            result = cursor.fetchall()
        finally:
            conn.close()
        

    return render_template('search_user.html', result=result)

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not all([username, password, role]):
            flash("Missing required fields: username, password, and role", "error")
            return redirect(url_for('create_user'))

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Add new user to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            conn.commit()
            flash(f"User '{username}' with role '{role}' created successfully.", "success")
            return redirect(url_for('create_user'))
        except sqlite3.Error as e:
            conn.rollback()
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('create_user'))
        finally:
            conn.close()
    
    # Render the HTML form for a GET request
    return render_template('create_user.html')

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
