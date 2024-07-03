from django.db import models, transaction
import logging

logger = logging.getLogger(__name__)


class PointsMixin(models.Model):
    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(points__gte=0),
                name="%(app_label)s_%(class)s_points_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(interest__gte=0),
                name="%(app_label)s_%(class)s_interest_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(disinterest__gte=0),
                name="%(app_label)s_%(class)s_disinterest_gte_0",
            ),
        ]

    points = models.IntegerField(default=0)
    interest = models.IntegerField(default=0)
    disinterest = models.IntegerField(default=0)

    def increment_points(self):
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            obj.points += 1
            obj.save()

    def decrement_points(self):
        logger.debug("decrementing points")
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            if obj.points > 0:
                obj.points -= 1
                obj.save()

    def increment_interest(self):
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            obj.interest += 1
            obj.save()

    def decrement_interest(self):
        logger.debug("decrementing interest")
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            if obj.interest > 0:
                obj.interest -= 1
                obj.save()

    def increment_disinterest(self):
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            obj.disinterest += 1
            obj.save()

    def decrement_disinterest(self):
        logger.debug("decrementing interest")
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            if obj.disinterest > 0:
                obj.disinterest -= 1
                obj.save()
