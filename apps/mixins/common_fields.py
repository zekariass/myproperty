from django.db import models
from django.utils import timezone

class DescriptionAndAddedOnFieldMixin(models.Model):
    """
    Common fields added to most models
    """
    description = models.TextField(default="")
    added_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class AddedOnFieldMixin(models.Model):
    """
    Common fields added to most models
    """
    added_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class ExpireOnFieldMixin(models.Model):
    """
    Common fields added to most models
    """
    expire_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class StartAndExpireOnFieldMixin(models.Model):
    """
    Common fields added to most models
    """
    start_on = models.DateTimeField(default=timezone.now)
    expire_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True