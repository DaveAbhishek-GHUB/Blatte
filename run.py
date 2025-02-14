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
from werkzeug.security import generate_password_hash, check_password_hash

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
    # Check if user is logged in
    user_email = request.cookies.get('user_email')
    if user_email:
        # Fetch user data similar to my_profile route
        conn = get_db_connection()
        if not conn:
            flash('System error: Unable to load profile', 'error')
            return redirect(url_for('index'))
            
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT firstname, lastname, email, carted, ordered 
                    FROM users 
                    WHERE email = %s
                """, (user_email,))
                user = cursor.fetchone()
                
                if not user:
                    flash('User not found', 'error')
                    return redirect(url_for('index'))
                
                # Parse JSON arrays and get counts
                carted_items = json.loads(user['carted']) if user['carted'] else []
                ordered_items = json.loads(user['ordered']) if user['ordered'] else []
                
                user_data = {
                    'name': f"{user['firstname']} {user['lastname']}",
                    'email': user['email'],
                    'carted_count': len(carted_items),
                    'ordered_count': len(ordered_items)
                }
                
                return render_template('auth.html', user=user_data)
                
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            flash('Error loading profile data', 'error')
            return redirect(url_for('index'))
        finally:
            if conn:
                conn.close()
    
    # If user is not logged in, render auth page normally
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

            # Create new user record with hashed password and initialized JSON fields
            insert_query = """
                INSERT INTO users 
                (firstname, lastname, email, password, wishlist, carted, ordered)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['firstname'],
                form_data['lastname'],
                form_data['email'],
                generate_password_hash(form_data['password']),
                '[]',  # Empty JSON array for wishlist
                '[]',  # Empty JSON array for carted
                '[]'   # Empty JSON array for ordered
            ))

            # Set authentication cookie and redirect
            response = make_response(redirect(url_for('index')))
            response.set_cookie('user_email', form_data['email'], httponly=True)
            flash('Registration successful: Welcome to BLATTÉ', 'success')
            return response

    except mysql.connector.Error as db_error:
        print(f"Database operation failed: {db_error}")
        flash('System error: Registration temporarily unavailable', 'error')
        return redirect(url_for('register'))
    finally:
        if conn:
            conn.close()

@app.route('/user/login', methods=['POST'])
def login_user():
    """Authenticate existing users with credential validation."""
    conn = get_db_connection()
    if not conn:
        flash('System error: Login temporarily unavailable', 'error')
        return redirect(url_for('auth'))

    try:
        credentials = {
            'email': request.form['email'],
            'password': request.form['password']
        }

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT email, password FROM users 
                WHERE email = %s
            """, (credentials['email'],))
            
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], credentials['password']):
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

@app.route('/admins/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        try:
            # Get form data
            product_data = {
                'product_name': request.form['product_name'],
                'price': float(request.form['price']),
                'product_category': request.form['product_category'],
                'description': json.dumps(request.form.getlist('description[]')),
                'ingredients': json.dumps(request.form.getlist('ingredients[]')),
                'brewing_notes': json.dumps(request.form.getlist('brewing_notes[]')),
                'main_product_image': request.form['main_product_image'],
                'additional_images': json.dumps(request.form.getlist('additional_images[]')),
                'weight': request.form['weight'],
                'dimensions': request.form['dimensions'],
                'availability_status': request.form['availability_status'],
                'discount_percentage': int(request.form['discount_percentage'] or 0)
            }

            conn = get_db_connection()
            if not conn:
                flash('Database connection error', 'error')
                return redirect(url_for('dashboard'))

            with conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO products (
                        product_name, price, product_category, description,
                        ingredients, brewing_notes, main_product_image,
                        additional_images, weight, dimensions,
                        availability_status, discount_percentage
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                cursor.execute(insert_query, (
                    product_data['product_name'],
                    product_data['price'],
                    product_data['product_category'],
                    product_data['description'],
                    product_data['ingredients'],
                    product_data['brewing_notes'],
                    product_data['main_product_image'],
                    product_data['additional_images'],
                    product_data['weight'],
                    product_data['dimensions'],
                    product_data['availability_status'],
                    product_data['discount_percentage']
                ))
                conn.commit()

            flash(f"Product '{product_data['product_name']}' has been added successfully!", 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            print(f"Error adding product: {e}")
            flash(f'Error adding product: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
        finally:
            if conn:
                conn.close()
    else:
        # Render the dashboard template
        return render_template('admins/dashboard.html')
    
@app.route('/productDetails/<int:id>')
def product_details(id):
    """Product details page with dynamic product loading."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('productDetails.html', product=None)
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Add print statement for debugging
            print(f"Fetching product with ID: {id}")
            
            cursor.execute("""
                SELECT * FROM products 
                WHERE id = %s
            """, (id,))
            product = cursor.fetchone()
            
            # Add debug print
            print(f"Found product: {product}")
            
            if not product:
                flash('Product not found', 'error')
                return redirect(url_for('index'))
            
            # Parse JSON strings to Python objects with null checks
            product['description'] = json.loads(product['description']) if product['description'] else []
            product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
            product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
            product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('productDetails.html', product=product)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading product details', 'error')
        return render_template('productDetails.html', product=None)
    finally:
        if conn:
            conn.close()

@app.template_filter('price_per_kg')
def price_per_kg_filter(price, weight):
    """Calculate price per kg, handling invalid inputs gracefully"""
    try:
        weight_float = float(weight)
        if weight_float <= 0:
            return None
        return float(price) / weight_float * 1000
    except (ValueError, TypeError, ZeroDivisionError):
        return None

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':

    app.run(
        debug=True,  # TODO: Disable in production environment
        host='0.0.0.0',
        port=5000
    )
