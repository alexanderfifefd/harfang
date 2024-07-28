# analytics/tasks.py
from celery import shared_task
from .models import Event, EventType, EngagementType
from django.utils import timezone


@shared_task
def log_event_task(
    user_id,
    session_id,
    event_type,
    engagement_type,
    url,
    referrer,
    user_agent,
    ip_address,
    metadata,
    engagement_score,
):
    Event.objects.create(
        user_id=user_id,
        session_id=session_id,
        event_type=EventType(event_type),
        engagement_type=EngagementType(engagement_type),
        url=url,
        referrer=referrer,
        user_agent=user_agent,
        ip_address=ip_address,
        event_time=timezone.now(),
        metadata=metadata,
        created_at=timezone.now(),
        engagement_score=engagement_score,
    )
