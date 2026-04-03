from app.models.audit import AuditLog

def log_action(db, user_id, action, metadata=None):
    log = AuditLog(
        user_id=user_id,
        action=action,
        metadata=metadata
    )
    db.add(log)
    db.commit()