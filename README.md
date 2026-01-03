# Vulpy - Vulnerable Web Application Lab

![ASVS 5.0](https://img.shields.io/badge/ASVS-5.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-TiiZss-yellow.svg)](https://www.buymeacoffee.com/TiiZss)

**Vulpy** is a Web Application Security Lab built with Python, Flask, and SQLite. It demonstrates the contrast between insecure ("Bad") and secure ("Good") coding practices, now updated to align with **OWASP ASVS 5.0**.

> **Note**: This is a modernized fork of the original [Vulpy](https://github.com/fportantier/vulpy) by [Fabian Portantier](https://github.com/fportantier). Special thanks for creating this excellent educational tool!

## 🎯 Project Overview

This lab provides two versions of the same application:

*   **😈 Vulpy Bad**: Intentionally vulnerable. Contains SQL Injection, XSS, CSRF, Weak Session Management, and more. A [Cheat Sheet](cheat_sheet_bad.md) is included for educational exploitation.
*   **🛡️ Vulpy Good**: Secured version. Patched against OWASP ASVS 5.0 standards, featuring parameterized queries, secure headers, CSRF protection, and robust session management.

## 🚀 Quick Start (Docker)

The easiest way to run Vulpy is using Docker Compose.

```bash
git clone https://github.com/TiiZss/vulpy.git
cd vulpy
docker-compose up -d --build
```

### Access the Applications

*   **Vulpy Bad**: [http://localhost:5002](http://localhost:5002)
*   **Vulpy Good**: [http://localhost:5003](http://localhost:5003)

## 🛠️ Features & Vulnerabilities

| Feature | Bad Version (Vulnerable) | Good Version (Secured) |
| :--- | :--- | :--- |
| **Database** | SQL Injection (String Formatting) | Parameterized Queries (ASVS 5.3.4) |
| **XSS** | Unescaped Input (`\| safe`) | Context-Aware Encoding |
| **CSRF** | No Protection | `Flask-WTF` CSRF Tokens (ASVS 4.2.2) |
| **Sessions** | Base64 JSON (Tamperable) | Signed, Secure, HttpOnly Cookies |
| **Secrets** | Hardcoded Keys | Environment Variables |
| **Headers** | Missing | Security Headers (X-Frame, CSP) |

## 📚 Documentation

*   [**Cheat Sheet (Bad Version)**](cheat_sheet_bad.md): Guide to exploiting the vulnerabilities.
*   [**Changelog**](CHANGELOG.md): History of changes and security fixes.
*   [**OWASP ASVS 5.0**](owasp-asvs-5.0.csv): The verification standard used for the "Good" version.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

---
*Maintained by TiiZss. Based on the work of fportantier.*
