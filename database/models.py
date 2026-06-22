from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    secure_records = db.relationship(
        "SecureRecord",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

    capability_tokens = db.relationship(
        "CapabilityToken",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    audit_logs = db.relationship(
        "AuditLog",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class SecureRecord(db.Model):
    __tablename__ = "secure_records"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    encrypted_data = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class CapabilityToken(db.Model):
    __tablename__ = "capability_tokens"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    token_hash = db.Column(
        db.String(255),
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    event_type = db.Column(
        db.String(100),
        nullable=False
    )

    event_details = db.Column(
        db.Text,
        nullable=False
    )

    ip_address = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )