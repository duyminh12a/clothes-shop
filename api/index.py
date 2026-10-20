import os
import sys
from pathlib import Path

# Add project root and apps directory to sys.path
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR / 'apps') not in sys.path:
    sys.path.insert(0, str(BASE_DIR / 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('VERCEL', '1')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
