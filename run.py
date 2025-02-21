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
    make_response,
    jsonify
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
    """Serve the main landing page template with different product categories."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('index.html', 
                             random_products=[],
                             gift_sets=[],
                             accessories=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch random products
            cursor.execute("""
                SELECT * FROM products 
                ORDER BY RAND() 
                LIMIT 4
            """)
            random_products = cursor.fetchall()

            # Fetch gift sets
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Gift Set'
                ORDER BY created_at DESC 
                LIMIT 4
            """)
            gift_sets = cursor.fetchall()

            # Fetch tea accessories
            cursor.execute("""
                SELECT * FROM products 
                WHERE product_category = 'Tea Accessories'
                ORDER BY created_at DESC 
                LIMIT 4
            """)
            accessories = cursor.fetchall()

            # Parse JSON strings to Python objects for all product sets
            for products in [random_products, gift_sets, accessories]:
                for product in products:
                    product['description'] = json.loads(product['description']) if product['description'] else []
                    product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                    product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                    product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []

            return render_template('index.html', 
                                random_products=random_products,
                                gift_sets=gift_sets,
                                accessories=accessories)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('index.html', 
                             random_products=[],
                             gift_sets=[],
                             accessories=[])
    finally:
        if conn:
            conn.close()

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
                WHERE product_category = 'Gift Set'
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
                (firstname, lastname, email, password, wishlist, carted, ordered, payment_methods, addresses)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['firstname'],
                form_data['lastname'],
                form_data['email'],
                generate_password_hash(form_data['password']),
                '[]',  # Empty JSON array for wishlist
                '[]',  # Empty JSON array for carted
                '[]',  # Empty JSON array for ordered
                '[]',  # Empty JSON array for payment_methods
                '[]'   # Empty JSON array for addresses
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

# Add new route to fetch saved user data
@app.route('/api/user/saved-data')
def get_saved_user_data():
    """Fetch saved addresses and payment methods for the logged-in user."""
    user_email = request.cookies.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection error'}), 500

    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT addresses, payment_methods 
                FROM users 
                WHERE email = %s
            """, (user_email,))
            user_data = cursor.fetchone()

            if not user_data:
                return jsonify({'success': False, 'message': 'User not found'}), 404

            return jsonify({
                'success': True,
                'addresses': json.loads(user_data['addresses']) if user_data['addresses'] else [],
                'payment_methods': json.loads(user_data['payment_methods']) if user_data['payment_methods'] else []
            })

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'message': 'Database error'}), 500
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
                SELECT email, password, firstname, lastname FROM users 
                WHERE email = %s
            """, (credentials['email'],))
            
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], credentials['password']):
                response = make_response(redirect(url_for('index')))
                response.set_cookie('user_email', credentials['email'], httponly=True)
                # Set user's full name in a cookie and add debug print
                full_name = f"{user['firstname']} {user['lastname']}"
                print(f"Setting user_name cookie to: {full_name}")  # Debug print
                response.set_cookie('user_name', full_name, httponly=True)
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
    response.delete_cookie('user_name')  # Also delete the name cookie
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
    # Check if user is logged in
    user_email = request.cookies.get('user_email')
    if not user_email:
        flash('Please login to view your wishlist', 'error')
        return redirect(url_for('auth'))
        
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('wishlist.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # First get user's wishlist
            cursor.execute("SELECT wishlist FROM users WHERE email = %s", (user_email,))
            user = cursor.fetchone()
            
            if not user or not user['wishlist']:
                return render_template('wishlist.html', products=[])
                
            # Parse wishlist JSON array
            wishlist_ids = json.loads(user['wishlist'])
            
            if not wishlist_ids:
                return render_template('wishlist.html', products=[])
            
            # Fetch products that are in the wishlist
            placeholders = ', '.join(['%s'] * len(wishlist_ids))
            cursor.execute(f"""
                SELECT * FROM products 
                WHERE id IN ({placeholders})
                ORDER BY FIELD(id, {placeholders})
            """, wishlist_ids + wishlist_ids)  # Pass IDs twice for IN and FIELD
            
            products = cursor.fetchall()
            
            # Parse JSON fields for each product
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []
            
            return render_template('wishlist.html', products=products)
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading wishlist', 'error')
        return render_template('wishlist.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/api/cart/<int:product_id>', methods=['GET', 'POST', 'DELETE'])
def toggle_cart(product_id):
    """Add, remove, or check product in user's cart."""
    user_email = request.cookies.get('user_email')
    if not user_email:
        return jsonify({'success': False, 'message': 'Please login first'}), 401
        
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Get current cart
            cursor.execute("SELECT carted FROM users WHERE email = %s", (user_email,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
                
            # Initialize empty cart if None
            current_cart = user['carted'] if user['carted'] else '[]'
            cart = json.loads(current_cart)
            
            if request.method == 'DELETE':
                # Remove product from cart
                if product_id in cart:
                    cart.remove(product_id)
                    message = 'Product removed from cart'
                else:
                    message = 'Product not in cart'
                
                # Update cart in database
                cursor.execute("""
                    UPDATE users 
                    SET carted = %s 
                    WHERE email = %s
                """, (json.dumps(cart), user_email))
                conn.commit()
                
                return jsonify({
                    'success': True,
                    'message': message
                })
            
            elif request.method == 'POST':
                # Add product to cart if not already present
                if product_id not in cart:
                    cart.append(product_id)
                    message = 'Product added to cart'
                    in_cart = True
                    
                    # Update cart in database
                    cursor.execute("""
                        UPDATE users 
                        SET carted = %s 
                        WHERE email = %s
                    """, (json.dumps(cart), user_email))
                    conn.commit()
                else:
                    message = 'Product already in cart'
                    in_cart = True
            else:  # GET request
                in_cart = product_id in cart
                message = 'Cart status checked'
            
            return jsonify({
                'success': True, 
                'message': message,
                'in_cart': in_cart
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/cart')
def cart():
    """Shopping cart management page."""
    # Check if user is logged in
    user_email = request.cookies.get('user_email')
    if not user_email:
        flash('Please login to view your cart', 'error')
        return redirect(url_for('auth'))
        
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('cart.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # First get user's cart
            cursor.execute("SELECT carted FROM users WHERE email = %s", (user_email,))
            user = cursor.fetchone()
            
            if not user or not user['carted']:
                return render_template('cart.html', products=[])
                
            # Parse cart JSON array
            cart_ids = json.loads(user['carted'])
            
            if not cart_ids:
                return render_template('cart.html', products=[])
            
            # Fetch products that are in the cart
            placeholders = ', '.join(['%s'] * len(cart_ids))
            cursor.execute(f"""
                SELECT * FROM products 
                WHERE id IN ({placeholders})
                ORDER BY FIELD(id, {placeholders})
            """, cart_ids + cart_ids)  # Pass IDs twice for IN and FIELD
            
            products = cursor.fetchall()
            
            # Parse JSON fields for each product
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []
            
            return render_template('cart.html', products=products)
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading cart', 'error')
        return render_template('cart.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/products')
def products():
    """Shopping products page with showcase of 16 products from all categories."""
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('products.html', products=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Fetch 2 products from each category (8 categories × 2 = 16 products)
            cursor.execute("""
                SELECT p.*
                FROM (
                    SELECT *,
                           ROW_NUMBER() OVER (PARTITION BY product_category ORDER BY created_at DESC) as rn
                    FROM products
                ) p
                WHERE p.rn <= 2
                ORDER BY p.product_category, p.created_at DESC
            """)
            
            products = cursor.fetchall()
            
            # Parse JSON fields for each product
            for product in products:
                product['description'] = json.loads(product['description']) if product['description'] else []
                product['additional_images'] = json.loads(product['additional_images']) if product['additional_images'] else []
                product['ingredients'] = json.loads(product['ingredients']) if product['ingredients'] else []
                product['brewing_notes'] = json.loads(product['brewing_notes']) if product['brewing_notes'] else []
            
            return render_template('products.html', products=products)
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading products', 'error')
        return render_template('products.html', products=[])
    finally:
        if conn:
            conn.close()

@app.route('/checkout')
def checkout():
    """Shopping checkout page with dynamic cart items."""
    user_email = request.cookies.get('user_email')
    if not user_email:
        flash('Please login to proceed with checkout', 'error')
        return redirect(url_for('auth'))
        
    conn = get_db_connection()
    if not conn:
        flash('Error connecting to database', 'error')
        return render_template('checkout.html', cart_items=[])
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Get user's cart items
            cursor.execute("SELECT carted FROM users WHERE email = %s", (user_email,))
            user = cursor.fetchone()
            
            if not user or not user['carted']:
                return render_template('checkout.html', cart_items=[])
                
            # Parse cart JSON array
            cart_ids = json.loads(user['carted'])
            
            if not cart_ids:
                return render_template('checkout.html', cart_items=[])
            
            # Fetch products in cart
            placeholders = ', '.join(['%s'] * len(cart_ids))
            cursor.execute(f"""
                SELECT id, product_name, price, main_product_image, 
                       product_category, weight, availability_status 
                FROM products 
                WHERE id IN ({placeholders})
                ORDER BY FIELD(id, {placeholders})
            """, cart_ids + cart_ids)
            
            cart_items = cursor.fetchall()
            
            # Calculate total
            subtotal = sum(item['price'] for item in cart_items)
            
            return render_template('checkout.html', 
                                 cart_items=cart_items,
                                 subtotal=subtotal,
                                 total=subtotal)  # Remove VAT, total equals subtotal
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading cart items', 'error')
        return render_template('checkout.html', cart_items=[])
    finally:
        if conn:
            conn.close()

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    """Handle checkout form submission with the new user table structure"""
    user_email = request.cookies.get('user_email')
    if not user_email:
        flash('Please login to complete checkout', 'error')
        return redirect(url_for('auth'))

    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('checkout'))

    try:
        with conn.cursor(dictionary=True) as cursor:
            # Get current user data
            cursor.execute("""
                SELECT carted, payment_methods, addresses, ordered 
                FROM users 
                WHERE email = %s
            """, (user_email,))
            user_data = cursor.fetchone()

            if not user_data:
                flash('User not found', 'error')
                return redirect(url_for('checkout'))

            # Parse existing JSON data
            payment_methods = json.loads(user_data['payment_methods']) if user_data['payment_methods'] else []
            addresses = json.loads(user_data['addresses']) if user_data['addresses'] else []
            cart_items = json.loads(user_data['carted']) if user_data['carted'] else []
            ordered_items = json.loads(user_data['ordered']) if user_data['ordered'] else []

            # Create new payment method and address from form data
            payment_method = request.form.get('payment_method', 'card')
            new_payment_method = create_payment_method(request.form, payment_method, len(payment_methods))
            new_address = create_address(request.form, len(addresses))

            # Get cart items details
            if not cart_items:
                flash('Your cart is empty', 'error')
                return redirect(url_for('cart'))

            # Create new order with fetched product details
            new_order = create_order(cart_items, new_payment_method, new_address, cursor)

            # Add order status
            new_order['status'] = 'inProgress'  # Set the order status to "inProgress"

            # Update user data
            payment_methods.append(new_payment_method)
            addresses.append(new_address)
            ordered_items.append(new_order)

            # Update database
            cursor.execute("""
                UPDATE users 
                SET payment_methods = %s,
                    addresses = %s,
                    ordered = %s,
                    carted = '[]'
                WHERE email = %s
            """, (
                json.dumps(payment_methods),
                json.dumps(addresses),
                json.dumps(ordered_items),
                user_email
            ))
            conn.commit()

            flash('Order placed successfully!', 'success')
            return redirect(url_for('order'))

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error processing order', 'error')
        return redirect(url_for('checkout'))
    finally:
        if conn:
            conn.close()

# Helper functions for checkout process
def create_payment_method(form_data, payment_type, method_id):
    """Create a payment method object from form data"""
    payment_method = {
        "id": method_id + 1,
        "type": payment_type
    }

    if payment_type == 'card':
        payment_method.update({
            "card_number": form_data.get('cardNumber', ''),
            "expiry": form_data.get('expiryDate', ''),
            "cvv": form_data.get('cvv', '')
        })
    elif payment_type == 'bank':
        payment_method.update({
            "bank_name": form_data.get('bankName', ''),
            "account_number": form_data.get('accountNumber', ''),
            "ifsc": form_data.get('ifscCode', '')
        })

    return payment_method

def create_address(form_data, address_id):
    """Create an address object from form data"""
    return {
        "id": address_id + 1,
        "house_number": form_data.get('houseNo', ''),
        "street": form_data.get('street', ''),
        "city": form_data.get('city', ''),
        "state": form_data.get('state', ''),
        "pincode": form_data.get('pincode', ''),
        "country": form_data.get('country', ''),
        "phone": form_data.get('phone', ''),
        "alt_phone": form_data.get('altPhone', '')
    }

def create_order(cart_items, payment_method, shipping_address, cursor):
    """Create an order object with product details"""
    placeholders = ', '.join(['%s'] * len(cart_items))
    cursor.execute(f"""
        SELECT id, product_name, price 
        FROM products 
        WHERE id IN ({placeholders})
    """, cart_items)
    products = cursor.fetchall()

    return {
        "order_id": datetime.now().strftime('%Y%m%d%H%M%S'),
        "products": [{
            "product_id": product['id'],
            "name": product['product_name'],
            "price": str(product['price']),
            "quantity": 1
        } for product in products],
        "total_amount": str(sum(product['price'] for product in products)),
        "payment": {
            "method_id": payment_method['id'],
            "type": payment_method['type'],
            "details": payment_method
        },
        "payment_status": True,
        "shipping_address": shipping_address,
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/order')
def order():
    """Shopping order management page."""
    return render_template('order.html')

@app.route('/myorders')
def myorders():
    """Track & trace order management page."""
    return render_template('myorders.html')

@app.route('/admins/dashboard')
def dashboard():
    """Admin dashboard with user management."""
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return render_template('admins/dashboard.html')
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Get total users count
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = cursor.fetchone()['total']
            
            # Get users with cart items count
            cursor.execute("SELECT COUNT(*) as active FROM users WHERE JSON_LENGTH(carted) > 0")
            active_carts = cursor.fetchone()['active']
            
            # Get total orders count
            cursor.execute("SELECT SUM(JSON_LENGTH(ordered)) as total FROM users")
            total_orders = cursor.fetchone()['total'] or 0
            
            # Fetch all users with their data
            cursor.execute("""
                SELECT 
                    id, 
                    firstname, 
                    lastname, 
                    email, 
                    JSON_LENGTH(wishlist) as wishlist_count,
                    JSON_LENGTH(carted) as cart_count,
                    JSON_LENGTH(ordered) as order_count,
                    created_at
                FROM users
                ORDER BY created_at DESC
            """)
            users = cursor.fetchall()
            
            return render_template('admins/dashboard.html', 
                                 users=users,
                                 total_users=total_users,
                                 active_carts=active_carts,
                                 total_orders=total_orders)
                                 
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading user data', 'error')
        return render_template('admins/dashboard.html')
    finally:
        if conn:
            conn.close()

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

@app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user and return JSON response."""
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
    try:
        with conn.cursor() as cursor:
            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if not cursor.fetchone():
                return jsonify({'success': False, 'message': 'User not found'}), 404
                
            # Delete the user
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            
            return jsonify({'success': True, 'message': 'User deleted successfully'})
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'success': False, 'message': 'Database error occurred'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/wishlist/<int:product_id>', methods=['GET', 'POST'])
def toggle_wishlist(product_id):
    """Add or remove product from user's wishlist."""
    print(f"Received {request.method} request for product ID: {product_id}")  # Debug log
    
    user_email = request.cookies.get('user_email')
    if not user_email:
        print("No user email found in cookies")  # Debug log
        return jsonify({'success': False, 'message': 'Please login first'}), 401
        
    print(f"User email: {user_email}")  # Debug log
    
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")  # Debug log
        return jsonify({'success': False, 'message': 'Database connection error'}), 500
        
    try:
        with conn.cursor(dictionary=True) as cursor:
            # Get current wishlist
            cursor.execute("SELECT wishlist FROM users WHERE email = %s", (user_email,))
            user = cursor.fetchone()
            
            if not user:
                print(f"No user found for email: {user_email}")  # Debug log
                return jsonify({'success': False, 'message': 'User not found'}), 404
                
            # Initialize empty wishlist if None
            current_wishlist = user['wishlist'] if user['wishlist'] else '[]'
            wishlist = json.loads(current_wishlist)
            print(f"Current wishlist: {wishlist}")  # Debug log
            
            if request.method == 'POST':
                # Toggle product in wishlist
                if product_id in wishlist:
                    wishlist.remove(product_id)
                    message = 'Product removed from wishlist'
                    in_wishlist = False
                else:
                    wishlist.append(product_id)
                    message = 'Product added to wishlist'
                    in_wishlist = True
                
                print(f"Updated wishlist: {wishlist}")  # Debug log
                
                # Update wishlist in database
                cursor.execute("""
                    UPDATE users 
                    SET wishlist = %s 
                    WHERE email = %s
                """, (json.dumps(wishlist), user_email))
                conn.commit()
                
                print(f"Database updated. Message: {message}")  # Debug log
            else:  # GET request
                in_wishlist = product_id in wishlist
                message = 'Wishlist status checked'
            
            response_data = {
                'success': True, 
                'message': message,
                'in_wishlist': in_wishlist
            }
            print(f"Sending response: {response_data}")  # Debug log
            return jsonify(response_data)
            
    except Exception as e:
        print(f"Error in wishlist operation: {e}")  # Debug log
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/admins/add-product', methods=['POST'])
def add_product():
    """Handle new product submission from admin dashboard."""
    conn = None  # Initialize conn before try block
    try:
        # Get form data
        product_data = {
            'product_name': request.form['product_name'],
            'price': float(request.form['price']),  # This should remain float
            'weight': request.form.get('weight', ''),  # Make weight optional
            'product_category': request.form['product_category'],
            'description': json.dumps(request.form.getlist('description[]')),
            'ingredients': json.dumps(request.form.getlist('ingredients[]')),
            'brewing_notes': json.dumps(request.form.getlist('brewing_notes[]')),
            'main_product_image': request.form['main_product_image'],
            'additional_images': json.dumps(request.form.getlist('additional_images[]')),
            'availability_status': request.form['availability_status']
        }

        conn = get_db_connection()
        if not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('dashboard'))

        with conn.cursor() as cursor:
            # Insert new product
            insert_query = """
                INSERT INTO products (
                    product_name, price, weight, product_category,
                    description, ingredients, brewing_notes,
                    main_product_image, additional_images,
                    availability_status, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
                )
            """
            cursor.execute(insert_query, (
                product_data['product_name'],
                product_data['price'],
                product_data['weight'] or None,  # Handle empty weight
                product_data['product_category'],
                product_data['description'],
                product_data['ingredients'],
                product_data['brewing_notes'],
                product_data['main_product_image'],
                product_data['additional_images'],
                product_data['availability_status']
            ))
            conn.commit()

        flash('Product added successfully', 'success')
        return redirect(url_for('dashboard'))

    except Exception as e:
        print(f"Error adding product: {e}")
        flash('Error adding product', 'error')
        return redirect(url_for('dashboard'))
    finally:
        if conn:
            conn.close()

@app.route('/debug/cookies')
def debug_cookies():
    """Debug route to check cookies"""
    return jsonify({
        'user_email': request.cookies.get('user_email'),
        'user_name': request.cookies.get('user_name')
    })

@app.route('/my_profile')
def my_profile():
    """User profile page with personalized data."""
    user_email = request.cookies.get('user_email')
    if not user_email:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('auth'))
        
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
            
            return render_template('utilities/myprofile.html', user=user_data)
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        flash('Error loading profile data', 'error')
        return redirect(url_for('index'))
    finally:
        if conn:
            conn.close()

# ========== APPLICATION ENTRY POINT ==========
if __name__ == '__main__':

    app.run(
        debug=True,  # TODO: Disable in production environment
        host='0.0.0.0',
        port=5000
    )
