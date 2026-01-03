import json
import base64

import geoip2.database

from cryptography.fernet import Fernet


from cryptography.fernet import Fernet
import os

# VULNERABILITY FIX: Hardcoded Cryptographic Key
# ASVS 5.0 3.5.2: Verify that secrets are not hardcoded.
# PREVIOUSLY: The encryption key was hardcoded in the source.
# NOW: We load it from environment variables or use a generated one (for demo purposes only).
# In production, this must be a persistent env var.
key = os.environ.get('SESSION_ENC_KEY', Fernet.generate_key().decode())
fernet = Fernet(key)
ttl = 7200 # seconds
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')


def getcountry(request):

    country = 'XX' # For local connections

    try:
        geo = reader.country(request.remote_addr)
        country = geo.country.iso_code
    except Exception:
        pass

    return country


def create(request, response, username):

    country = getcountry(request)

    # VULNERABILITY FIX: Insecure Cookie Attributes
    # ASVS 5.0 3.4.1: Verify cookie attributes (Secure, HttpOnly, SameSite).
    # PREVIOUSLY: Cookies lacked HttpOnly, Secure, and SameSite attributes.
    # NOW: We set them explicitly.
    response.set_cookie('vulpy_session', fernet.encrypt(
        (username + '|' + country).encode()
    ), httponly=True, samesite='Lax', secure=True)

    return response


def load(request):

    cookie = request.cookies.get('vulpy_session')

    if not cookie:
        return {}

    try:
        token = fernet.decrypt(cookie.encode(), ttl=ttl).decode()
        username, country = token.split('|')
    except Exception as e:
        print(e)
        return {}

    if country == getcountry(request.remote_addr):
        return {'username': username, 'country' : country}
    else:
        return {}


def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response

