from datetime import datetime, timezone


def utcnow() -> datetime:
    """Naive UTC now. Every DateTime column stores naive UTC so SQLite and Postgres behave the same."""
    return datetime.now(timezone.utc).replace(tzinfo=None)