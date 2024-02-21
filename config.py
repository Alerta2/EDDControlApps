import os
import django
import sys
import pandas as pd

path = 'D:\OneDrive\LARUEX-ALERTA2\Desarrollos\Monitoriza\MONITORIZA'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoConfig.settings')
django.setup()

# now you can import the settings and access them
from django.conf import settings