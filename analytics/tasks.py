# analytics/tasks.py
from celery import shared_task
from .models import Event


@shared_task
def log_event_task(
    user_id, session_id, event_type, url, referrer, user_agent, ip_address, metadata
):
    Event.objects.create(
        user_id=user_id,
        session_id=session_id,
        event_type=event_type,
        url=url,
        referrer=referrer,
        user_agent=user_agent,
        ip_address=ip_address,
        metadata=metadata,
    )
