# Flask App Login, Registration, and Audit Log Features

## Features Added

1. **Password Hashing**: User passwords are now securely hashed using Werkzeug before being stored in the database.
2. **User Registration**: New users can register via `/register`. Admins can add users from `/admin/users`.
3. **Admin User Management**: Admins can view, add, and delete users at `/admin/users`.
4. **Audit Logging**: All login, logout, registration, and admin actions are logged in the `audit_log` table. Admins can view logs at `/admin/audit_log`.

## Setup Instructions

1. **Install dependencies** (if not already):
   ```bash
   pip install flask werkzeug
   ```
2. **Initialize the database** (creates users, clusters, and audit_log tables):
   ```bash
   python3 apps/flask-app/init_db.py
   ```
3. **Run the Flask app**:
   ```bash
   python3 apps/flask-app/app.py
   ```
4. **Access the app**:
   - Login: `/login` (admin/adminpass, viewer/viewerpass by default)
   - Register: `/register`
   - Dashboard: `/dashboard`
   - Admin user management: `/admin/users` (admin only)
   - Audit log: `/admin/audit_log` (admin only)

## Notes
- Passwords are never stored in plaintext.
- Only admins can add/delete users and view audit logs.
- All user and admin actions are recorded for auditing.
