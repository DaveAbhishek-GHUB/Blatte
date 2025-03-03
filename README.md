# Blatté - Premium Tea E-commerce Platform

## Overview
Blatté is a sophisticated e-commerce platform specializing in premium tea products and accessories. Built with Flask and MySQL, it offers a comprehensive shopping experience for tea enthusiasts, featuring various tea categories, gift sets, and accessories.

## Features

### Customer Features
- **Product Browsing**
  - Browse various tea categories (Green, Black, Oolong, Herbal, Fruit)
  - View detailed product information with descriptions and brewing notes
  - Search functionality for products
  - Filter products by category

### Shopping Features
- **Shopping Cart**
  - Add/remove products
  - Update quantities
  - Real-time price calculations

- **Wishlist**
  - Save favorite items
  - Easy transfer to cart

- **User Accounts**
  - Personal profile management
  - Order history tracking
  - Address management
  - Payment method storage

### Admin Features
- **Dashboard**
  - User management
  - Order tracking
  - Product management
  - Sales analytics

## Technical Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Custom session management with secure cookie handling

### Frontend
- HTML5, CSS3, JavaScript
- Responsive design for mobile compatibility

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd blatte
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL:
- Create a database named 'blatte'
- Update DB_CONFIG in run.py with your MySQL credentials

5. Initialize the database:
```bash
mysql -u root -p blatte < schema.sql
```

6. Start the application:
```bash
python run.py
```

## Database Configuration

The application supports multiple MySQL port configurations (3306, 3307, 3308, 3309) and will attempt to connect to available ports automatically. Default configuration:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'blatte',
    'port': 3308
}
```

## Security Features
- Password hashing for user accounts
- Secure session management
- CSRF protection
- Input validation and sanitization
- Admin authentication middleware

## API Endpoints

### Product Management
- `/products` - List all products
- `/productDetails/<id>` - Get product details
- `/api/search-products` - Search products

### User Management
- `/auth` - Authentication gateway
- `/register` - User registration
- `/user/login` - User login
- `/user/logout` - User logout

### Shopping Features
- `/cart` - Shopping cart management
- `/wishlist` - Wishlist management
- `/checkout` - Checkout process
- `/myorders` - Order tracking

### Admin Routes
- `/admins/dashboard` - Admin dashboard
- `/admin/orders` - Order management
- `/admin/add-product` - Product addition
- `/admin/delete-product/<id>` - Product deletion

## Environment Variables
For production deployment, configure the following:
- `SECRET_KEY` - Flask session security
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
