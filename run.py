"""
BLATTÉ Web Application Main Module
Version: 1.0
Maintainer: DevOps Team
"""

# ========== STANDARD LIBRARY IMPORTS ==========
from datetime import datetime

# ========== THIRD-PARTY LIBRARY IMPORTS ==========
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import mysql.connector

# ========== FLASK APPLICATION INITIALIZATION ==========
app = Flask(__name__)
app.secret_key = 'BlatteADP'  # In production, use environment variable for secret key

# ========== DATABASE CONFIGURATION ==========
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blatte',
    'port': 3308,
    'autocommit': True  # Ensure automatic commit for transactions
}

# Initialize database connection pool
try:
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        print("Database connection established successfully")
except mysql.connector.Error as err:
    print(f"Database connection error: {err}")
    print("Action required: Verify MySQL service status and connection parameters")

# ========== PRODUCT CATALOG ROUTES ==========
@app.route('/')
def index():
    """Serve the main landing page template."""
    return render_template('index.html')

@app.route('/teaBlends')
def tea_blends():
    """Display tea blends product category page."""
    return render_template('teaBlends.html')

@app.route('/giftSets')
def gift_sets():
    """Render gift sets collection page."""
    return render_template('giftSets.html')

# ========== TEA CATEGORY ROUTES ==========
@app.route('/greenTea')
def green_tea():
    """Green tea product category page."""
    return render_template('greenTea.html')

@app.route('/herbalTea')
def herbal_tea():
    """Herbal tea product category page."""
    return render_template('herbalTea.html')

@app.route('/blackTea')
def black_tea():
    """Black tea product category page."""
    return render_template('blackTea.html')

@app.route('/oolongTea')
def oolong_tea():
    """Oolong tea product category page."""
    return render_template('oolongTea.html')

@app.route('/fruitTea')
def fruit_tea():
    """Fruit-infused tea products page."""
    return render_template('fruitTea.html')

@app.route('/teaAccessories')
def tea_accessories():
    """Tea-related accessories and equipment page."""
    return render_template('teaAccessories.html')

# ========== USER AUTHENTICATION ROUTES ==========
@app.route('/auth')
def auth():
    """Authentication gateway page (login/registration)."""
    return render_template('auth.html')

@app.route('/register')
def register():
    """User registration page with validation checks."""
    if request.cookies.get('user_email'):
        flash('Authentication conflict: User already logged in', 'error')
        return redirect(url_for('index'))
    return render_template('utilities/register.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    """Handle new user registration with data validation."""
    form_data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm-password']
    }

    if form_data['password'] != form_data['confirm_password']:
        flash('Password validation failed: Mismatched credentials', 'error')
        return redirect(url_for('register'))

    try:
        with conn.cursor() as cursor:
            # Check existing user conflict
            cursor.execute("SELECT email FROM users WHERE email = %s", (form_data['email'],))
            if cursor.fetchone():
                flash('Account conflict: Email already registered', 'error')
                return redirect(url_for('register'))

            # Insert new user record
            insert_query = """
                INSERT INTO users 
                (firstname, lastname, email, password, createdat)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['firstname'],
                form_data['lastname'],
                form_data['email'],
                form_data['password'],
                datetime.now()
            ))

            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_email', form_data['email'], httponly=True)
            flash('Registration successful: Welcome to BLATTÉ', 'success')
            return response

    except mysql.connector.Error as db_error:
        print(f"Database operation failed: {db_error}")
        flash('System error: Registration temporarily unavailable', 'error')
        return redirect(url_for('index'))

@app.route('/user/login', methods=['POST'])
def login_user():
    """Authenticate existing users with credential validation."""
    try:
        credentials = {
            'email': request.form['email'],
            'password': request.form['password']
        }

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT email FROM users 
                WHERE email = %s AND password = %s
            """, (credentials['email'], credentials['password']))
            
            if cursor.fetchone():
                response = make_response(redirect(url_for('index')))
                response.set_cookie('user_email', credentials['email'], httponly=True)
                flash('Authentication successful: Welcome back', 'success')
                return response
            
            flash('Authentication failed: Invalid credentials', 'error')
            return redirect(url_for('auth'))

    except Exception as auth_error:
        print(f"Authentication system error: {auth_error}")
        flash('System error: Login temporarily unavailable', 'error')
        return redirect(url_for('auth'))

@app.route('/user/logout')
def logout_user():
    """Terminate user session and clear authentication cookies."""
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_email')
    flash('Session terminated: Successfully logged out', 'success')
    return response

# ========== SUPPORTING PAGES ROUTES ==========
@app.route('/about')
def about():
    """Company information and brand story page."""
    return render_template('about.html')

@app.route('/store')
def store():
    """Physical store locator and information page."""
    return render_template('store.html')

@app.route('/career')
def career():
    """Career opportunities and job listings page."""
    return render_template('career.html')

@app.route('/blatteforcompanies')
def corporate_services():
    """B2B and corporate gifting solutions page."""
    return render_template('blatteforcompanies.html')

# ========== CUSTOMER SUPPORT ROUTES ==========
@app.route('/Pressinquiries')
def press_inquiries():
    """Media and press relations contact page."""
    return render_template('Pressinquiries.html')

@app.route('/Contact')
def contact():
    """General customer support contact page."""
    return render_template('Contact.html')

@app.route('/Trackandtrace')
def order_tracking():
    """Order tracking and shipment status page."""
    return render_template('Trackandtrace.html')

@app.route('/ShippingPayment')
def shipping_info():
    """Shipping options and payment methods information page."""
    return render_template('ShippingPayment.html')

@app.route('/wishlist')
def wishlist():
    """User-curated product wishlist management page."""
    return render_template('wishlist.html')

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':
    app.run(
        debug=True,  # Disable in production environment
        host='0.0.0.0',
        port=5000
    )
