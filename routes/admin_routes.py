from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from database.models import AuditLog, User, SecureRecord
from services.token_service import validate_capability_token
from services.audit_service import log_security_event

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_capability_required():
    raw_token = session.get("capability_token")

    if not validate_capability_token(current_user.id, raw_token):
        log_security_event(
            "UNAUTHORIZED_ADMIN_ACCESS",
            "Invalid capability token used for admin route.",
            current_user.id
        )

        flash("Secure session expired. Please log in again.")
        return False

    if current_user.role != "admin":
        log_security_event(
            "ADMIN_ACCESS_DENIED",
            "Non-admin user attempted to access admin dashboard.",
            current_user.id
        )

        flash("Admin access is required.")
        return False

    return True


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if not admin_capability_required():
        return redirect(url_for("user.dashboard"))

    total_users = User.query.count()
    total_records = SecureRecord.query.count()

    security_alerts = AuditLog.query.filter(
        AuditLog.event_type.in_([
            "SQL_INJECTION_ALERT",
            "UNAUTHORIZED_ACCESS",
            "LOGIN_FAILED",
            "ADMIN_ACCESS_DENIED"
        ])
    ).count()

    recent_logs = AuditLog.query.order_by(
        AuditLog.created_at.desc()
    ).limit(20).all()

    return render_template(
        "audit_logs.html",
        total_users=total_users,
        total_records=total_records,
        security_alerts=security_alerts,
        logs=recent_logs
    )