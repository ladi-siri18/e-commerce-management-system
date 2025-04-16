import os

# Configuration values for database and other settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
DATABASE_URI = 'sqlite:///estore.db'
