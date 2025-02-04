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

@app.route('/greenTea')
def greenTea():
    """
    Render the greenTea.html template when user visits the greenTea page
    Returns: rendered greenTea.html template
    """
    return render_template('greenTea.html')
@app.route('/auth')
def auth():
    """
    Render the auth.html template when user visits the auth page
    Returns: rendered auth.html template
    """
    return render_template('auth.html')

@app.route('/register')
def register():
    """
    Render the register.html template when user visits the register page
    Returns: rendered register.html template if not logged in, redirects to index if logged in
    """
    if request.cookies.get('user_email'):
        flash('You are already registered and logged in', 'error')
        return redirect(url_for('index'))
    return render_template('utilities/register.html')


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

@app.route('/user/logout')
def logout_user():
    """
    Handle user logout
    Returns: redirect to index page
    """
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_email')
    flash('Successfully logged out!', 'success')
    return response

@app.route('/about')
def about():
    """
    Render the about.html template when user visits the about page
    Returns: rendered about.html template
    """
    return render_template('about.html')

@app.route('/store')
def store():
    """
    Render the store.html template when user visits the store page
    Returns: rendered store.html template
    """
    return render_template('store.html')

@app.route('/career')
def career():
    """
    Render the career.html template when user visits the career page
    Returns: rendered career.html template
    """
    return render_template('career.html')

@app.route('/blatteforcompanies')
def blatteforcompanies():
    """
    Render the blatteforcompanies.html template when user visits the blatteforcompanies page
    Returns: rendered blatteforcompanies.html template
    """
    return render_template('blatteforcompanies.html')

@app.route('/Pressinquiries')
def Pressinquiries():
    """
    Render the Pressinquiries.html template when user visits the Pressinquiries page
    Returns: rendered Pressinquiries.html template
    """
    return render_template('Pressinquiries.html')

@app.route('/Contact')
def Contact():
    """
    Render the Contact.html template when user visits the Contact page
    Returns: rendered Contact.html template
    """
    return render_template('Contact.html')

@app.route('/Trackandtrace')
def Trackandtrace():
    """
    Render the Trackandtrace.html template when user visits the Trackandtrace page
    Returns: rendered Trackandtrace.html template
    """
    return render_template('Trackandtrace.html')

@app.route('/ShippingPayment')
def ShippingPayment():
    """
    Render the ShippingPayment.html template when user visits the ShippingPayment page
    Returns: rendered ShippingPayment.html template
    """
    return render_template('ShippingPayment.html')


# Main entry point
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
