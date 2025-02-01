# Import required modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from datetime import datetime
import mysql.connector

# Initialize Flask application
app = Flask(__name__)

# Set secret key for session management and security
app.secret_key = 'BlatteADP'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blatte',
    'port': 3308
}

# Create database connection
try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Successfully connected to database")
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    print("Please ensure MySQL server is running")

# Define route for homepage
@app.route('/')
def index():
    """
    Render the index.html template when user visits homepage
    Returns: rendered index.html template
    """
    return render_template('index.html')

@app.route('/teaBlends')
def teaBlends():
    """
    Render the teaBlends.html template when user visits the teaBlends page
    Returns: rendered teaBlends.html template
    """
    return render_template('teaBlends.html')

@app.route('/giftSets')
def giftSets():
    """
    Render the giftSets.html template when user visits the giftSets page
    Returns: rendered giftSets.html template
    """
    return render_template('giftSets.html')

@app.route('/register')
def register():
    """
    Render the register.html template when user visits the register page
    Returns: rendered register.html template
    """
    return render_template('register.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    """
    Handle user registration form submission
    Returns: redirect to login page on success or back to register on failure
    """
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Validate if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        try:
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))

            # Insert new user into database with current timestamp
            sql = "INSERT INTO users (firstname, lastname, email, password, createdat) VALUES (%s, %s, %s, %s, %s)"
            current_time = datetime.now()
            cursor.execute(sql, (firstname, lastname, email, password, current_time))
            conn.commit()
            cursor.close()

            # Create response object with redirect to index page
            response = make_response(redirect(url_for('index')))
            # Set cookie with user's email
            response.set_cookie('user_email', email)

            flash('Registration successful!', 'success')
            return response

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('An error occurred during registration', 'error')
            return redirect(url_for('index'))

@app.route('/login')
def login():
    """
    Render the login.html template when user visits the login page
    Returns: rendered login.html template
    """
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def login_user():
    """
    Handle user login form submission
    Returns: redirect to index page on success or back to login on failure
    """
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                response = make_response(redirect(url_for('index')))
                response.set_cookie('user_email', email)
                flash('Successfully logged in!', 'success')
                return response
            else:
                flash('Invalid email or password', 'error')
                return redirect(url_for('login'))
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login', 'error')
            return redirect(url_for('login'))

# Main entry point
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
