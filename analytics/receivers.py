# analytics/receivers.py
from django.dispatch import receiver
from .signals import event_logged
from .tasks import log_event_task
from .models import EventType, EngagementType


@receiver(event_logged)
def log_event(sender, **kwargs):
    log_event_task.delay(
        user_id=kwargs.get("user_id", ""),
        session_id=kwargs.get("session_id", ""),
        event_type=kwargs.get("event_type", EventType.CUSTOM),
        engagement_type=kwargs.get("engagement_type", EngagementType.NONE),
        url=kwargs.get("url", ""),
        referrer=kwargs.get("referrer", ""),
        user_agent=kwargs.get("user_agent", ""),
        ip_address=kwargs.get("ip_address", ""),
        metadata=kwargs.get("metadata", {}),
        engagement_score=kwargs.get("engagement_score", None),
    )
