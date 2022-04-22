import os

# URL that the json POST will be sent to
SEND_URL = "https://webhook.site/9a227568-3994-4c29-9006-0762865b808b"

# email and email passwords
FROM_EMAIL = os.environ.get('GEAR_EMAIL')
FROM_PASS = os.environ.get('GEAR_PASS')
TO_EMAIL = FROM_EMAIL

# Oauth tokens
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
