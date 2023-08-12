from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q

from apps.agents import models as agent_models
from apps.properties import models as prop_models
from apps.payments import models as pay_models
from apps.mixins import constants
from apps.mixins.common_fields import (
    AddedOnFieldMixin,
    DescriptionAndAddedOnFieldMixin,
    ExpireOnFieldMixin,
)
from apps.system import models as sys_models


class Listing(DescriptionAndAddedOnFieldMixin, ExpireOnFieldMixin):
    listing_type = models.CharField(max_length=30, choices=constants.LISTING_TYPES)
    listing_payment_type = models.CharField(
        max_length=30, choices=constants.LISTING_PAYMENT_TYPES
    )
    property_price = models.DecimalField(
        max_digits=20, decimal_places=5, default=0.00000
    )
    property_price_currency = models.ForeignKey(
        sys_models.Currency, on_delete=models.SET_NULL, null=True
    )
    is_active = models.BooleanField(default=True)
    agent_branch = models.ForeignKey(agent_models.AgentBranch, on_delete=models.CASCADE)
    main_property = models.ForeignKey(prop_models.Property, on_delete=models.CASCADE)
    listing_payment = models.ForeignKey(
        pay_models.Payment,
        on_delete=models.SET_NULL,
        related_name="listings",
        null=True,
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    is_listed_by_subscription = models.BooleanField(default=False)
    featuring_payment = models.ForeignKey(
        pay_models.Payment,
        on_delete=models.SET_NULL,
        related_name="featured_listings",
        null=True,
        blank=True,
    )
    featured_on = models.DateTimeField(null=True, blank=True)

    @property
    def is_expired(self):
        return timezone.now() > self.expire_on

    @property
    def is_approved(self):
        return self.listing_payment.is_approved if self.listing_payment else False

    @property
    def is_featuring_approved(self):
        return self.featuring_payment.is_approved if self.featuring_payment else False

    @property
    def agent(self):
        return f"{self.agent_branch.agent}"

    def __str__(self) -> str:
        return f"{self.id}: {self.listing_type}"

    def save(self, *args, **kwargs):
        # CHECK IF FEATURING IS APPROVED BUT FEATURING PAUMENT AND FEATURING DATE IS NULL
        if self.is_featuring_approved and (
            not self.featured_on or not self.featuring_payment
        ):
            raise ValidationError(
                "featured_on or featuring_payment should not be null, featuring is approved!"
            )

        # CHECK IF NON MULTI UNIT PROPERTY HAS ACTIVE LEASTING ALREADY
        # MULTI-UNIT MAIN PROPERTY MAY HAVE MORE THAN ONE LISTING, EACH LISTING FOR ONE UNIT
        query1 = Q(main_property__property_category__cat_key=constants.APARTMENT_KEY)
        query2 = Q(
            main_property__property_category__cat_key=constants.COMMERCIAL_PROPERTY_KEY
        )

        active_listings_for_this_property = Listing.objects.filter(
            main_property=self.main_property, expire_on__gt=timezone.now()
        ).exclude(Q(query1 | query2))

        # RAISE VALIDATION ERROR IF PROPERTY WITH ACTIVE LISTING IS PRESENT
        if active_listings_for_this_property:
            raise ValidationError(
                f"There is active listing already for property with id {self.main_property}"
            )
        return super().save(*args, **kwargs)


class CommonListingMixin(AddedOnFieldMixin):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RentListing(CommonListingMixin):
    rent_payment_period = models.CharField(max_length=20, choices=constants.PERIODS)
    rent_term = models.CharField(max_length=20, choices=constants.RENT_TERM)
    deposit_amount = models.DecimalField(
        max_digits=20, decimal_places=5, default=0.00000
    )


class SaleListing(CommonListingMixin):
    ...


# class ApartmentListing(CommonListingMixin):
#     apartment = models.ForeignKey(prop_models.Apartment, on_delete=models.CASCADE)


class ApartmentUnitListing(CommonListingMixin):
    # apartment_listing = models.ForeignKey(ApartmentListing, on_delete=models.CASCADE)
    apartment_unit = models.ForeignKey(
        prop_models.ApartmentUnit, on_delete=models.CASCADE
    )
    apartment = models.ForeignKey(prop_models.Apartment, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # CHECK IF UNIT PROPERTY HAS ACTIVE LEASTING ALREADY
        active_listings_for_this_unit = ApartmentUnitListing.objects.filter(
            apartment_unit=self.apartment_unit,
            listing__expire_on__gt=timezone.now(),
        )

        # RAISE VALIDATION ERROR IF UNIT PROPERTY WITH ACTIVE LISTING IS PRESENT
        if active_listings_for_this_unit:
            raise ValidationError(
                f"There is active listing already for property unit with id {self.apartment_unit}"
            )
        return super().save(*args, **kwargs)


class VillaListing(CommonListingMixin):
    villa = models.ForeignKey(prop_models.Villa, on_delete=models.CASCADE)


class CondominiumListing(CommonListingMixin):
    condominium = models.ForeignKey(prop_models.Condominium, on_delete=models.CASCADE)


class TownhouseListing(CommonListingMixin):
    townhouse = models.ForeignKey(prop_models.Townhouse, on_delete=models.CASCADE)


class SharehouseListing(CommonListingMixin):
    sharehouse = models.ForeignKey(prop_models.Sharehouse, on_delete=models.CASCADE)


# class RoomListing(CommonListingMixin):
#     # sharehouse_listing = models.ForeignKey(SharehouseListing, on_delete=models.CASCADE)
#     room = models.ForeignKey(prop_models.Room, on_delete=models.CASCADE)
#     sharehouse = models.ForeignKey(prop_models.Sharehouse, on_delete=models.CASCADE)


class VenueListing(CommonListingMixin):
    venue = models.ForeignKey(prop_models.Venue, on_delete=models.CASCADE)


class LandListing(CommonListingMixin):
    land = models.ForeignKey(prop_models.Land, on_delete=models.CASCADE)


# class CommercialPropertyListing(CommonListingMixin):
#     commercial_property = models.ForeignKey(
#         prop_models.CommercialProperty, on_delete=models.CASCADE
#     )


class OfficeListing(CommonListingMixin):
    # commercial_property_listing = models.ForeignKey(
    #     CommercialPropertyListing, on_delete=models.CASCADE
    # )
    office_unit = models.ForeignKey(prop_models.OfficeUnit, on_delete=models.CASCADE)
    commercial_property = models.ForeignKey(
        prop_models.CommercialProperty, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # CHECK IF UNIT PROPERTY HAS ACTIVE LEASTING ALREADY
        active_listings_for_this_unit = OfficeListing.objects.filter(
            office_unit=self.office_unit,
            listing__expire_on__gt=timezone.now(),
        )

        # RAISE VALIDATION ERROR IF UNIT PROPERTY WITH ACTIVE LISTING IS PRESENT
        if active_listings_for_this_unit:
            raise ValidationError(
                f"There is active listing already for property unit with id {self.office_unit}"
            )
        return super().save(*args, **kwargs)


class OtherCommercialPropertyUnitListing(CommonListingMixin):
    # commercial_property_listing = models.ForeignKey(
    #     CommercialPropertyListing, on_delete=models.CASCADE
    # )
    other_commercial_property_unit = models.ForeignKey(
        prop_models.OtherCommercialPropertyUnit, on_delete=models.CASCADE
    )
    commercial_property = models.ForeignKey(
        prop_models.CommercialProperty, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        # CHECK IF UNIT PROPERTY HAS ACTIVE LEASTING ALREADY
        active_listings_for_this_unit = (
            OtherCommercialPropertyUnitListing.objects.filter(
                other_commercial_property_unit=self.other_commercial_property_unit,
                listing__expire_on__gt=timezone.now(),
            )
        )

        # RAISE VALIDATION ERROR IF UNIT PROPERTY WITH ACTIVE LISTING IS PRESENT
        if active_listings_for_this_unit:
            raise ValidationError(
                f"There is active listing already for property unit with id {self.other_commercial_property_unit}"
            )
        return super().save(*args, **kwargs)


class SavedListing(AddedOnFieldMixin):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
