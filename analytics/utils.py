# analytics/utils.py
from .signals import event_logged
from .models import EventType, EngagementType


def log_event(
    request,
    event_type=EventType.CUSTOM,
    engagement_type=EngagementType.NONE,
    metadata=None,
    engagement_score=None,
):
    if metadata is None:
        metadata = {}

    user_id = request.user.id if request.user.is_authenticated else "anonymous"
    session_id = request.session.session_key
    url = request.build_absolute_uri()
    referrer = request.META.get("HTTP_REFERER", "")
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    ip_address = request.META.get("REMOTE_ADDR", "")

    event_logged.send(
        sender="log_event",
        user_id=user_id,
        session_id=session_id,
        event_type=event_type,
        engagement_type=engagement_type,
        url=url,
        referrer=referrer,
        user_agent=user_agent,
        ip_address=ip_address,
        metadata=metadata,
        engagement_score=engagement_score,
    )
