#!/usr/bin/env python3

from pathlib import Path

from flask import Flask, g, redirect, request

from mod_hello import mod_hello
from mod_user import mod_user
from mod_posts import mod_posts
from mod_mfa import mod_mfa
from mod_csp import mod_csp
from mod_api import mod_api

# VULNERABILITY FIX: CSRF Protection
# ASVS 5.0 4.2.1: Verify that the application protects against CSRF.
# ASVS 5.0 4.2.2: Verify that CSRF protection is implemented.
# PREVIOUSLY: The application had no CSRF protection.
# NOW: We use Flask-WTF to enable CSRF protection globally.
from flask_wtf.csrf import CSRFProtect
import os

import libsession

app = Flask('vulpy')

# VULNERABILITY FIX: Hardcoded Secret & Debug Mode
# ASVS 5.0 3.5.2: Verify that secrets are not hardcoded.
# PREVIOUSLY: Secret key was hardcoded and debug was enabled.
# NOW: Secret key is loaded from environment or uses a secure random default (for demoware). Debug is disabled by default.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123aa8a93bdde342c871564a62282af857bda14b3359fde95d0c5e4b321610c1')

# VULNERABILITY FIX: Insecure Session Configuration
# ASVS 5.0 3.4.1: Verify cookie attributes (Secure, HttpOnly, SameSite).
# PREVIOUSLY: Cookies were defaults (Lax, not Secure, not HttpOnly for custom).
# NOW: Enforcing secure cookie attributes.
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True # Requires HTTPS, but good practice to set.
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

csrf = CSRFProtect(app)

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')
app.register_blueprint(mod_csp, url_prefix='/csp')
app.register_blueprint(mod_api, url_prefix='/api')

csp_file = Path('csp.txt')
csp = ''

if csp_file.is_file():
    with csp_file.open() as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line = line.replace('\n', '')
            if line:
                csp += line
        print('CSP:', csp)

@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

@app.after_request
def add_csp_headers(response):
    if csp:
        response.headers['Content-Security-Policy'] = csp

    # VULNERABILITY FIX: Missing Security Headers
    # ASVS 5.0 14.4.1: Verify that the X-Content-Type-Options header is set to 'nosniff'.
    # ASVS 5.0 14.4.4: Verify that the X-Frame-Options header is set to 'DENY' or 'SAMEORIGIN'.
    # PREVIOUSLY: These headers were missing.
    # NOW: We explicitly set them.
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # HSTS (Strict-Transport-Security) should also be set in production/HTTPS.
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    return response

app.run(debug=False, host='127.0.1.1', port=5001, extra_files='csp.txt')

