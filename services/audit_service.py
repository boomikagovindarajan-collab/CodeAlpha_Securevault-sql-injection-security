from flask import request
from extensions import db
from database.models import AuditLog


def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.remote_addr


def log_security_event(event_type, event_details, user_id=None):
    audit_log = AuditLog(
        user_id=user_id,
        event_type=event_type,
        event_details=event_details,
        ip_address=get_client_ip()
    )

    db.session.add(audit_log)
    db.session.commit()