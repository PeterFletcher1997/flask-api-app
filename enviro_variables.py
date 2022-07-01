import os

# URL that the json POST will be sent to
SEND_URL = "https://webhook.site/d02a90c7-71ad-45f8-9ba4-6acddc30887e"

# email and email passwords
FROM_EMAIL = os.environ.get('GEAR_EMAIL')
FROM_PASS = os.environ.get('GEAR_PASS')
TO_EMAIL = FROM_EMAIL

# Oauth tokens
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
