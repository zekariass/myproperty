from django.db import models
from apps.mixins.common_fields import AddedOnFieldMixin, DescriptionAndAddedOnFieldMixin


class Country(AddedOnFieldMixin):
    """Country models for countries used in the system"""

    name = models.CharField(
        "country name", max_length=100, unique=True, blank=False, null=False
    )
    iso_3166_code = models.CharField(
        "country code", max_length=30, null=True, blank=True
    )
    latitute = models.CharField("geo latitude", max_length=20, null=True, blank=True)
    longitude = models.CharField("geo logitude", max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name}"


class Address(AddedOnFieldMixin):
    """Address of a property or an agent"""

    street = models.CharField("street name", max_length=100, blank=False, null=False)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    house_number = models.CharField(
        "house number", max_length=10, blank=True, null=True
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(
        Country, blank=False, null=False, on_delete=models.CASCADE
    )
    latitude = models.CharField("geo latitude", max_length=20, null=True, blank=True)
    longitude = models.CharField("geo longitude", max_length=20, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "%s %s" % (self.street, self.post_code)


class Tag(DescriptionAndAddedOnFieldMixin):
    name = models.CharField("tag name", max_length=100)
    affixing_period_in_days = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.name}"


class TagApplyTo(AddedOnFieldMixin):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    apply_to = models.CharField("tag name", max_length=100)

    def __str__(self) -> str:
        return f"{self.tag.name} applies to: {self.apply_to}"
