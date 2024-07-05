# analytics/models.py
from django.db.models import CheckConstraint, IntegerChoices, Q
from django.utils import timezone
from clickhouse_backend import models


class EventType(IntegerChoices):
    PAGE_VIEW = 1
    CLICK = 2
    FORM_SUBMISSION = 3
    LOGIN = 4
    SIGNUP = 5
    CUSTOM = 99


class Event(models.ClickhouseModel):
    user_id = models.StringField(max_length=255, default="")
    session_id = models.StringField(max_length=255, default="")
    event_type = models.EnumField(choices=EventType.choices, default=EventType.CUSTOM)
    url = models.StringField(max_length=1024, default="", low_cardinality=True)
    referrer = models.StringField(max_length=1024, default="", low_cardinality=True)
    user_agent = models.StringField(max_length=1024, default="", low_cardinality=True)
    ip_address = models.GenericIPAddressField(default="::")
    event_time = models.DateTime64Field(default=timezone.now)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTime64Field(auto_now_add=True)

    class Meta:
        ordering = ["-event_time"]
        engine = models.MergeTree(
            primary_key="event_time",
            order_by=("event_time", "user_id"),
            partition_by=models.toYYYYMMDD("event_time"),
            index_granularity=1024,
            index_granularity_bytes=1 << 20,
            enable_mixed_granularity_parts=1,
        )
        indexes = [
            models.Index(
                fields=["user_id"],
                name="user_id_set_idx",
                type=models.Set(1000),
                granularity=4,
            ),
            models.Index(
                fields=["session_id"],
                name="session_id_set_idx",
                type=models.Set(1000),
                granularity=4,
            ),
            models.Index(
                fields=["ip_address"],
                name="ip_bloom_idx",
                type=models.BloomFilter(0.001),
                granularity=1,
            ),
        ]
        constraints = (
            CheckConstraint(
                name="event_time_non_future",
                check=Q(event_time__lte=timezone.now),
            ),
        )
