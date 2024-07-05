# analytics/receivers.py
from django.dispatch import receiver
from .signals import event_logged
from .tasks import log_event_task


@receiver(event_logged)
def log_event(sender, **kwargs):
    log_event_task.delay(
        user_id=kwargs.get("user_id", ""),
        session_id=kwargs.get("session_id", ""),
        event_type=kwargs.get("event_type", ""),
        url=kwargs.get("url", ""),
        referrer=kwargs.get("referrer", ""),
        user_agent=kwargs.get("user_agent", ""),
        ip_address=kwargs.get("ip_address", ""),
        metadata=kwargs.get("metadata", {}),
    )
