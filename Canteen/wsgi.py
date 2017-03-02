# -*- coding: utf-8 -*-
"""
WSGI config for Canteen project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

EXTRA_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

if EXTRA_DIR not in sys.path:
    sys.path.append(EXTRA_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Canteen.settings")

application = get_wsgi_application()
