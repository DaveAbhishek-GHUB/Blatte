"""
BLATTÉ Web Application Main Module

A Flask-based web application for an e-commerce tea shop.
Handles routing, database operations, and user authentication.

Version: 1.0
Maintainer: DevOps Team
"""

# ========== STANDARD LIBRARY IMPORTS ==========
from datetime import datetime
import json

# ========== THIRD-PARTY LIBRARY IMPORTS ==========
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response
)
import mysql.connector

# ========== FLASK APPLICATION INITIALIZATION ==========
app = Flask(__name__)
# TODO: Move secret key to environment variable in production
app.secret_key = 'BlatteADP'

# ========== DATABASE CONFIGURATION ==========
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blatte',
    'port': 3308,
    'autocommit': True  # Ensures automatic transaction commits
}

# ========== DATABASE CONNECTION FUNCTION ==========
def get_db_connection():
    """Create and return a new database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Database connection established successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        print("Action required: Verify MySQL service status and connection parameters")
        return None

# ========== PRODUCT CATALOG ROUTES ==========
@app.route('/')
def index():
    """Serve the main landing page template."""
    return render_template('index.html')

@app.route('/teaBlends')
def tea_blends():
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('teaBlends.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Tea Blends'
                ORDER BY created_at DESC
            """)
            products = cursor.fetchall()

            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('teaBlends.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('teaBlends.html', products=[])   
    finally:
        if conn:
            conn.close()

@app.route('/giftSets')
def gift_sets():
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('giftSets.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Gift Sets'
                ORDER BY created_at DESC
            """)
            products = cursor.fetchall()

            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else [] 

            return render_template('giftSets.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('giftSets.html', products=[])
    finally:
        if conn:
            conn.close()

# ========== TEA CATEGORY ROUTES ==========
@app.route('/greenTea')
def green_tea():
    """Green tea product category page."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('greenTea.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Green Tea'
                ORDER BY created_at DESC    
            """)
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []   
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('greenTea.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('greenTea.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/herbalTea')
def herbal_tea():
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('herbalTea.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Herbal Tea'
                ORDER BY created_at DESC
            """)
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('herbalTea.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('herbalTea.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/blackTea')
def black_tea():
    """Black tea product category page."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('blackTea.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all black tea products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Black Tea'
                ORDER BY created_at DESC
            """)
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []
                
            return render_template('blackTea.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('blackTea.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/oolongTea')
def oolong_tea():
    """Oolong tea product category page."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('oolongTea.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Oolong Tea'
                ORDER BY created_at DESC
            """)
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else [] 
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('oolongTea.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('oolongTea.html', products=[])
    finally:
        if conn:
            conn.close()    

@app.route('/fruitTea')
def fruit_tea():
    """Fruit-infused tea products page."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('fruitTea.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Fruit Tea'
                ORDER BY created_at DESC
            """)    
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('fruitTea.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('fruitTea.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/teaAccessories')
def tea_accessories():

    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('teaAccessories.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch all products, sorted by creation date
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Tea Accessories'
                ORDER BY created_at DESC
            """)    
            products = cursor.fetchall()
            
            # Parse JSON strings to Python objects with null checks
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('teaAccessories.html', products=products)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')    
        return render_template('teaAccessories.html', products=[])
    finally:
        if conn:
            conn.close()

# ========== USER AUTHENTICATION ROUTES ==========
@app.route('/auth')
def auth():
    """Authentication gateway page (login/registration)."""
    return render_template('auth.html')

@app.route('/register')
def register():
    """
    User registration page with validation checks.
    
    Redirects to index if user is already logged in.
    """
    if request.cookies.get('user_email'):
        flash('Authentication conflict: User already logged in', 'error')
        return redirect(url_for('index'))
    return render_template('utilities/register.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    """
    Handle new user registration with data validation.
    
    Validates form data, checks for existing users,
    and creates new user record in database.
    """
    form_data = {
        'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm-password']
    }

    # Validate password match
    if form_data['password'] != form_data['confirm_password']:
        flash('Password validation failed: Mismatched credentials', 'error')
        return redirect(url_for('register'))

    conn = get_db_connection()
    if not conn:
        flash('System error: Registration temporarily unavailable', 'error')
        return redirect(url_for('register'))

    try:
        with conn.cursor() as cursor:
            # Check for existing user
            cursor.execute("SELECT email FROM users WHERE email = %s", (form_data['email'],))
            if cursor.fetchone():
                flash('Account conflict: Email already registered', 'error')
                return redirect(url_for('register'))

            # Create new user record
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

            # Set authentication cookie and redirect
            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_email', form_data['email'], httponly=True)
            flash('Registration successful: Welcome to BLATTÉ', 'success')
            return response

    except mysql.connector.Error as db_error:
        print(f"Database operation failed: {db_error}")
        flash('System error: Registration temporarily unavailable', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

@app.route('/user/login', methods=['POST'])
def login_user():
    """
    Authenticate existing users with credential validation.
    
    Verifies user credentials against database and sets auth cookie.
    """
    conn = get_db_connection()
    if not conn:
        flash('System error: Login temporarily unavailable', 'error')
        return redirect(url_for('auth'))

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
    finally:
        if conn:
            conn.close()

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

@app.route('/cart')
def cart():
    """Shopping cart management page."""
    return render_template('cart.html')

@app.route('/Teapots')
def teapots():
    """Tea pot product category page."""
    return render_template('Teapots.html')

@app.route('/Cups-and-Mugs')
def cups_and_mugs():
    """Cups and mugs product category page."""
    return render_template('Cups-and-Mugs.html')

@app.route('/Preparation')
def preparation():
    """Preparation product category page."""
    return render_template('Preparation.html')

@app.route('/Kettles')
def kettles():
    """Kettles product category page."""
    return render_template('Kettles.html')

@app.route('/MatchaAccessories')
def matcha_accessories():
    """Matcha accessories product category page."""
    return render_template('MatchaAccessories.html')

@app.route('/OnTheGo')
def on_the_go():
    """On the go product category page."""
    return render_template('OnTheGo.html')

@app.route('/products')
def products():
    """Product showcase page."""
    return render_template('products.html')

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':

    app.run(
        debug=True,  # TODO: Disable in production environment
        host='0.0.0.0',
        port=5000
    )
