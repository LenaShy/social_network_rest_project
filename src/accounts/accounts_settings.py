from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)


EMAIL_HUNTER_API_KEY = get('EMAIL_HUNTER_API_KEY', 'your_key')
CLEARBIT_API_KEY = get('CLEARBIT_API_KEY', 'your_key')

