"""
WSGI Configurations
"""

import os

from django.core.wsgi import get_wsgi_application
try:
	from whitenoise import WhiteNoise  
except Exception:
	WhiteNoise = None

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

if WhiteNoise is not None:
	import os
	from django.conf import settings

	static_root = getattr(settings, "STATIC_ROOT", None)
	# Ensure the static root directory exists before passing to WhiteNoise.
	# WhiteNoise raises an error if the directory doesn't exist.
	if static_root:
		try:
			if not os.path.isdir(static_root):
				os.makedirs(static_root, exist_ok=True)
		except Exception:
			# If we cannot create the directory, skip wrapping to avoid crashing.
			static_root = None

	if static_root and os.path.isdir(static_root):
		application = WhiteNoise(application, root=static_root)
