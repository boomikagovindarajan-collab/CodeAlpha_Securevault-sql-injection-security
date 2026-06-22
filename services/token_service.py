import secrets
import hashlib
from datetime import datetime, timedelta
from extensions import db
from database.models import CapabilityToken


def hash_token(token):
    return hashlib.sha256(token.encode()).hexdigest()


def create_capability_token(user_id):
    raw_token = secrets.token_urlsafe(32)

    token_hash = hash_token(raw_token)

    expiry_time = datetime.utcnow() + timedelta(hours=2)

    capability_token = CapabilityToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expiry_time,
        is_active=True
    )

    db.session.add(capability_token)
    db.session.commit()

    return raw_token


def validate_capability_token(user_id, raw_token):
    if not raw_token:
        return False

    token_hash = hash_token(raw_token)

    token = CapabilityToken.query.filter_by(
        user_id=user_id,
        token_hash=token_hash,
        is_active=True
    ).first()

    if not token:
        return False

    if token.expires_at < datetime.utcnow():
        token.is_active = False
        db.session.commit()
        return False

    return True


def revoke_user_tokens(user_id):
    CapabilityToken.query.filter_by(
        user_id=user_id,
        is_active=True
    ).update({"is_active": False})

    db.session.commit()