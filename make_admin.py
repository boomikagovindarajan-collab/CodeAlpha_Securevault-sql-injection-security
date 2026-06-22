from app import app
from extensions import db
from database.models import User

username = "Boomika.06"   # Change this to the username you registered with

with app.app_context():
    user = User.query.filter_by(username=username).first()

    if user:
        user.role = "admin"
        db.session.commit()
        print(f"{username} is now an admin.")
    else:
        print("User not found. Check the username.")