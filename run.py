# Import required modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash

# Initialize Flask application
app = Flask(__name__)

# Set secret key for session management and security
app.secret_key = 'BlatteADP'

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

# Main entry point
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
