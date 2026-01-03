# Vulpy 2.0.1 - ASVS 5.0 Edition

This release marks a major overhaul of the Vulpy project, modernizing it and aligning the "Good" version with **OWASP ASVS 5.0**.

## ⚡ Key Differences from Original
This fork includes significant security updates compared to the original version:
- **OWASP ASVS 5.0**: Updated verification standard (was v4.0).
- **Global CSRF Protection**: Implemented `Flask-WTF` with hidden tokens in all forms.
- **Secure Session Management**: Enforced `HttpOnly`, `Secure`, and `SameSite` cookies.
- **No `| safe` Filters**: Removed insecure filters to enable auto-escaping.
- **Docker Support**: Streamlined deployment with Docker Compose.

## 🛡️ Security Fixes (Good Version)
- **SQL Injection**: Fixed via parameterized queries.
- **XSS**: Fixed via context-aware encoding.
- **CSRF**: Fixed via global token validation.
- **Session Hijacking**: Fixed via secure cookie attributes and signed sessions.

## 📚 Documentation
- Added **Cheat Sheet** (`cheat_sheet_bad.md`) for exploiting the "Bad" version.
- Added **Changelog**.
- Updated **README** with quick start guide.

**Full Changelog**: https://github.com/TiiZss/vulpy/commits/v2.0.1
