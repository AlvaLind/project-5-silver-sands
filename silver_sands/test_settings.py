import os
import sys
from pathlib import Path
from silver_sands.settings import *

# Fetch base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from env.py 
if os.path.isfile('env.py'):
    import env

# Middleware configuration (add additional middleware as needed)
MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Static files settings (if applicable)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use SQLite for testing
if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

# Set DEBUG to True for testing
DEBUG = True

# Test-specific configurations (optional)
# Configure allowed hosts for testing
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Email backend for testing (optional)
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Set other testing-related settings as needed
