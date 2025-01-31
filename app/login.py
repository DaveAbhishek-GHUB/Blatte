from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'blatte_db'
}

# MySQL Connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

# Dashboard Route (example page after login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Welcome, {session['user_name']}! This is your dashboard."
    else:
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
