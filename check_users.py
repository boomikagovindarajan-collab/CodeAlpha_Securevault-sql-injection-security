from app import app
from database.models import User

with app.app_context():
    users = User.query.all()

    if not users:
        print("No users found. Please register again.")
    else:
        for user in users:
            print(f"Username: {user.username} | Email: {user.email} | Role: {user.role}")