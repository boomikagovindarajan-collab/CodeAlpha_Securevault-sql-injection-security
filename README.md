# 🛡️ SecureVault  
### 🔐 Cloud-Based Data Security System with SQL Injection Protection

SecureVault is a professional Flask web application built to protect sensitive user data from SQL injection attacks, unauthorized access, and data leaks.

It combines secure authentication, AES-256 encryption, audit logging, and role-based access control in one cloud-ready system.

---

## 🧰 Technology Stack
| Technology | Purpose |
|---|---|
| 🐍 Python | Backend programming language |
| 🌶️ Flask | Web application framework |
| 🗄️ SQLAlchemy | Secure database ORM |
| 🔐 Flask-Login | User session management |
| 🛡️ Werkzeug | Password hashing |
| 🔒 AES-256 | Sensitive data encryption |
| 🧾 SQLite | Local database |
| 🎨 HTML & CSS | User interface design |
| ⚙️ Python-dotenv | Environment variable management |

---

## 📁 Project Structure

```text
securevault/
│
├── 📄 app.py
├── ⚙️ config.py
├── 🔌 extensions.py
├── 📦 requirements.txt
├── 🗃️ database/
├── 🛣️ routes/
├── 🛡️ services/
├── 🎨 static/
└── 📄 templates/

## 🧩 Main Modules

🏠 **Home Page**  
Provides an overview of SecureVault and its security features.

👤 **User Registration and Login**  
Allows users to create accounts, log in securely, and access their dashboard.

📁 **Secure Records**  
Allows users to add, view, and manage encrypted sensitive records.

📊 **Admin Dashboard**  
Allows administrators to monitor users, security alerts, and audit logs.

🚨 **Security Alerts**  
Tracks suspicious login and registration attempts for security monitoring.

🔐 **AES-256 Encryption Service**  
Encrypts sensitive data before it is stored in the database.

🎫 **Capability Token Service**  
Controls access to protected server features using secure tokens.

📋 **Audit Log Service**  
Records important actions such as registration, login, logout, failed attempts, and security alerts.

👩‍💻 **Author**
Boomika Govindarajan
🎓 B.Tech Information Technology Student
