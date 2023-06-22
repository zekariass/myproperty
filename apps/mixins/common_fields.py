from django.db import models
from django.core.validators import MinValueValidator 
from django.utils import timezone

from apps.mixins import constants

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


class PropertyStatusFieldMixin(models.Model):
    status = models.CharField("property status", max_length=30)

    class Meta:
        abstract = True


class CommonResidentialFieldsMixin(models.Model):
    bed_rooms = models.IntegerField("number of bed rooms", validators=[MinValueValidator(0)])
    bath_rooms = models.IntegerField("number of bath rooms", validators=[MinValueValidator(0)])
    floor = models.IntegerField("floor/storey level", default=0)
    area = models.DecimalField("housing area", max_digits=12, decimal_places=5)
    is_furnished = models.BooleanField(default=False)
    status = models.CharField("current status of the property", choices=constants.PROPERTY_STATUS, max_length=50)

    class Meta:
        abstract = True


class CommonPropertyShallowFieldsMixin():
    @property
    def agent(self):
        return f"{self.parent_property.agent_branch.agent}"
    
    @property
    def agent_branch(self):
        return f"{self.parent_property.agent_branch}"
    
    @property
    def cat_key(self):
        return f"{self.parent_property.cat_key}"
    