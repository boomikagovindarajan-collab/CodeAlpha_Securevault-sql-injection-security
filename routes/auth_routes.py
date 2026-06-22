from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from database.models import User
from services.security_service import contains_sql_injection_pattern, is_valid_username
from services.token_service import create_capability_token, revoke_user_tokens
from services.audit_service import log_security_event

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not is_valid_username(username):
            flash("Username must contain 3-30 letters, numbers, dots, or underscores.")
            return redirect(url_for("auth.register"))

        if contains_sql_injection_pattern(username) or contains_sql_injection_pattern(email):
            log_security_event(
                "SQL_INJECTION_ALERT",
                "Suspicious input blocked during registration."
            )
            flash("Suspicious request detected and blocked.")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        log_security_event(
            "USER_REGISTERED",
            f"New user account created: {username}",
            user.id
        )

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Security layer: blocks suspicious login input
        if contains_sql_injection_pattern(username):
            log_security_event(
                "SQL_INJECTION_ALERT",
                "Suspicious input blocked during login."
            )
            flash("Suspicious request detected and blocked.")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            log_security_event(
                "LOGIN_FAILED",
                f"Failed login attempt for username: {username}"
            )
            flash("Invalid username or password.")
            return redirect(url_for("auth.login"))

        login_user(user)

        revoke_user_tokens(user.id)
        raw_token = create_capability_token(user.id)
        session["capability_token"] = raw_token

        log_security_event(
            "LOGIN_SUCCESS",
            "User logged in successfully.",
            user.id
        )

        return redirect(url_for("user.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        revoke_user_tokens(current_user.id)

        log_security_event(
            "LOGOUT",
            "User logged out successfully.",
            current_user.id
        )

    session.pop("capability_token", None)
    logout_user()

    flash("You have been logged out.")
    return redirect(url_for("auth.login"))