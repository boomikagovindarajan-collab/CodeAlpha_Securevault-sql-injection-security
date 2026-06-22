from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from extensions import db
from database.models import SecureRecord
from services.encryption_service import encrypt_data, decrypt_data
from services.security_service import contains_sql_injection_pattern
from services.token_service import validate_capability_token
from services.audit_service import log_security_event

user_bp = Blueprint("user", __name__, url_prefix="/user")


def capability_required():
    """
    Verifies that the logged-in user has a valid capability token.
    """

    raw_token = session.get("capability_token")

    if not validate_capability_token(current_user.id, raw_token):
        log_security_event(
            "UNAUTHORIZED_ACCESS",
            "Invalid or expired capability token used.",
            current_user.id
        )

        flash("Your secure session has expired. Please log in again.")
        return False

    return True


@user_bp.route("/dashboard")
@login_required
def dashboard():
    if not capability_required():
        return redirect(url_for("auth.logout"))

    records = SecureRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(
        SecureRecord.created_at.desc()
    ).all()

    decrypted_records = []

    for record in records:
        try:
            decrypted_text = decrypt_data(record.encrypted_data)

            decrypted_records.append({
                "id": record.id,
                "data": decrypted_text,
                "created_at": record.created_at
            })

        except Exception:
            decrypted_records.append({
                "id": record.id,
                "data": "Unable to decrypt this record.",
                "created_at": record.created_at
            })

    return render_template(
        "dashboard.html",
        records=decrypted_records
    )


@user_bp.route("/add-record", methods=["GET", "POST"])
@login_required
def add_record():
    if not capability_required():
        return redirect(url_for("auth.logout"))

    if request.method == "POST":
        sensitive_data = request.form.get("sensitive_data", "").strip()

        if not sensitive_data:
            flash("Please enter confidential data before saving.")
            return redirect(url_for("user.add_record"))

        # This is an additional detection layer.
        # Parameterized/ORM database operations remain the main SQLi defense.
        if contains_sql_injection_pattern(sensitive_data):
            log_security_event(
                "SQL_INJECTION_ALERT",
                "Suspicious data input blocked while creating a secure record.",
                current_user.id
            )

            flash("Suspicious input detected. Record was not saved.")
            return redirect(url_for("user.add_record"))

        encrypted_text = encrypt_data(sensitive_data)

        secure_record = SecureRecord(
            user_id=current_user.id,
            encrypted_data=encrypted_text
        )

        db.session.add(secure_record)
        db.session.commit()

        log_security_event(
            "SECURE_RECORD_CREATED",
            "Sensitive record encrypted and stored successfully.",
            current_user.id
        )

        flash("Your confidential record was encrypted and stored securely.")
        return redirect(url_for("user.dashboard"))

    return render_template("add_record.html")


@user_bp.route("/delete-record/<int:record_id>", methods=["POST"])
@login_required
def delete_record(record_id):
    if not capability_required():
        return redirect(url_for("auth.logout"))

    record = SecureRecord.query.filter_by(
        id=record_id,
        user_id=current_user.id
    ).first()

    if not record:
        log_security_event(
            "UNAUTHORIZED_RECORD_ACCESS",
            f"Attempted access to record ID: {record_id}",
            current_user.id
        )

        flash("Record not found or access denied.")
        return redirect(url_for("user.dashboard"))

    db.session.delete(record)
    db.session.commit()

    log_security_event(
        "SECURE_RECORD_DELETED",
        f"Secure record ID {record_id} deleted.",
        current_user.id
    )

    flash("Secure record deleted successfully.")
    return redirect(url_for("user.dashboard"))