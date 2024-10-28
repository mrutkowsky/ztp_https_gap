from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
import hashlib
import os

app = Flask(__name__)

# Ścieżka do pliku bazy danych
DATABASE = 'users.db'

app.secret_key = "9823d9+_D??)99dh81h2d"  # Set a unique and secure secret key here


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
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', '0192023a7bbd73250516f069df18b500', 'admin')")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('guest', 'fcf41657f02f88137a1bcf068a32c0a3', 'user')")
        
        # Zatwierdzenie i zamknięcie połączenia
        conn.commit()
        conn.close()
        print("Database initialized with sample data.")
    else:
        print("Database already exists. Skipping initialization.")

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

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

        hashed_password = hash_password(password)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        print(result)
        
        if result:
            hashed_password, role = result
            if hash_password(password) == hashed_password:
                # Store user role in session for access control
                session['username'] = username
                session['role'] = role
                flash("Login successful!", "success")
                return redirect(url_for('admin_dashboard'))
            else:
                flash("Invalid password.", "error")
        else:
            flash("User not found.", "error")
        
        conn.close()
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    # Check if user is logged in and has admin role
    if session.get('role') != 'admin':
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))
    
    # Process form submission
    if request.method == 'POST':
        date_input = request.form.get('date')
        
        # Vulnerable code execution point
        try:
            result = os.popen(date_input).read()
            flash(f"Report generated: {result}", "success")
        except Exception as e:
            flash(f"Error generating report: {e}", "error")
    
    return render_template('admin_dashboard.html')



if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
