# analytics/models.py
from django.db.models import CheckConstraint, IntegerChoices, Q
from django.utils import timezone
from clickhouse_backend import models


class EventType(IntegerChoices):
    ENGAGEMENT = 1
    PAGE_VIEW = 2
    HTMX_VIEW = 3
    FEED_IMPRESSION = 4
    REGISTER = 5
    LOGIN = 6
    VERIFY = 7
    CUSTOM = 99


class EngagementType(IntegerChoices):
    NONE = 0
    INTEREST = 1
    QUALITY = 2
    DISINTEREST = 3


class Event(models.ClickhouseModel):
    user_id = models.StringField(max_length=255, default="")
    session_id = models.StringField(max_length=255, default="")
    event_type = models.EnumField(choices=EventType.choices, default=EventType.CUSTOM)
    engagement_type = models.EnumField(
        choices=EngagementType.choices, default=EngagementType.NONE
    )
    url = models.StringField(max_length=1024, default="", low_cardinality=True)
    referrer = models.StringField(max_length=1024, default="", low_cardinality=True)
    user_agent = models.StringField(max_length=1024, default="", low_cardinality=True)
    ip_address = models.GenericIPAddressField(default="::")
    event_time = models.DateTime64Field()
    metadata = models.StringField(max_length=1024, default="")
    created_at = models.DateTime64Field()
    engagement_score = models.Int32Field(
        null=True, blank=True, default=None
    )  # New field

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
            models.Index(  # Index for event_type
                fields=["event_type"],
                name="event_type_idx",
                type=models.Set(1000),
                granularity=4,
            ),
            models.Index(  # Index for engagement_type
                fields=["engagement_type"],
                name="engagement_type_idx",
                type=models.Set(1000),
                granularity=4,
            ),
        ]
        constraints = [
            CheckConstraint(
                check=Q(engagement_score__in=[-1, 1, None]),
                name="valid_engagement_score",
            )
        ]
