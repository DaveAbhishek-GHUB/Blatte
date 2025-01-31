from flask import Flask

# Specify the template folder explicitly
app = Flask(__name__, template_folder='../templates', static_folder='../static')

from app import routes