# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-01-03

### Security (Vulpy Good Version)
- **SQL Injection**: Fixed vulnerability in `libuser.py` by implementing parameterized queries for user creation and password changes.
- **XSS**: Eliminated Cross-Site Scripting vulnerabilities in `posts.view.html` and `messages.html` by removing the insecure `| safe` Jinja2 filter.
- **CSRF**: Implemented global Cross-Site Request Forgery protection using `Flask-WTF`. Added `csrf_token` hidden fields to all POST forms (`login`, `mfa`, `create`, `chpasswd`, `post`).
- **Session Management**:
    - Removed hardcoded encryption key in `libsession.py`; now generated securely or loaded from environment variables.
    - Enforced secure cookie attributes: `HttpOnly`, `Secure`, and `SameSite='Lax'`.
- **Configuration**:
    - Disabled `debug` mode in `vulpy.py` by default.
    - Moved `SECRET_KEY` to environment variables.
    - Added security headers: `X-Frame-Options: SAMEORIGIN` and `X-Content-Type-Options: nosniff`.

### Documentation
- **ASVS**: Updated OWASP Application Security Verification Standard (ASVS) reference from v4.0 to v5.0.
- **Cheat Sheet**: Added `cheat_sheet_bad.md` detailing exploitation vectors for the "Bad" version (SQLi, XSS, CSRF, Session Tampering).
- **Code Comments**: Added detailed in-code comments referencing specific ASVS 5.0 controls for every security fix.

### Infrastructure
- **Docker**: Fixed container name conflicts in `docker-compose.yml` and verified successful deployment of both `vulpy_bad` and `vulpy_good` containers.
