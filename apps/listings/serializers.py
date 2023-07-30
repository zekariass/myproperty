from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.mixins import constants

from . import models as listing_models


class RentListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.RentListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SaleListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.SaleListing
        fields = "__all__"
        read_only_fields = ["listing"]


class ListingSerializer(ModelSerializer):
    listing_type_data = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    is_approved = serializers.SerializerMethodField(read_only=True)
    is_featuring_approved = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = listing_models.Listing
        fields = [
            "id",
            "listing_type",
            "listing_payment_type",
            "property_price",
            "property_price_currency",
            "listing_payment",
            "is_approved",
            "is_expired",
            "is_active",
            "description",
            "is_featured",
            "featuring_payment",
            "featured_on",
            "is_featuring_approved",
            "listing_type_data",
            "agent_branch",
            "agent",
            "main_property",
            "expire_on",
            "added_on",
        ]
        read_only_fields = [
            "id",
            "added_on",
            "expire_on",
            "is_featured",
            "featured_on",
            "listing_payment",
            "featuring_payment",
            "is_featuring_approved",
            "main_property",
            "agent_branch",
            "agent",
        ]

    def get_listing_type_data(self, obj):
        if obj.listing_type == constants.LISTING_TYPE_RENT:
            rent_listing = listing_models.RentListing.objects.get(listing=obj.id)
            return RentListingSerializer(instance=rent_listing).data
        elif obj.listing_type == constants.LISTING_TYPE_SALE:
            sale_listing = listing_models.SaleListing.objects.get(listing=obj.id)
            return SaleListingSerializer(instance=sale_listing).data

    def get_is_approved(self, obj):
        return obj.is_approved

    def get_is_expired(self, obj):
        return obj.is_expired

    def get_is_featuring_approved(self, obj):
        return obj.is_featuring_approved

    def get_agent(self, obj):
        return obj.agent


class ApartmentUnitListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.ApartmentUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class CondominiumListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.CondominiumListing
        fields = "__all__"
        read_only_fields = ["listing"]


class VillaListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.VillaListing
        fields = "__all__"
        read_only_fields = ["listing"]


class TownhouseListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.TownhouseListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SharehouseListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.SharehouseListing
        fields = "__all__"
        read_only_fields = ["listing"]


# class RoomListingSerializer(ModelSerializer):
#     class Meta:
#         model = listing_models.RoomListing
#         fields = "__all__"
#         read_only_fields = ["listing"]


class VenueListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.VenueListing
        fields = "__all__"
        read_only_fields = ["listing"]


class LandListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.LandListing
        fields = "__all__"
        read_only_fields = ["listing"]


# class CommercialPropertyListingSerializer(ModelSerializer):
#     class Meta:
#         model = listing_models.CommercialPropertyListing
#         fields = "__all__"


class OfficeListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.OfficeListing
        fields = "__all__"
        read_only_fields = ["listing"]


class OtherCommercialPropertyUnitListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.OtherCommercialPropertyUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SavedListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.SavedListing
        fields = "__all__"
        read_only_fields = ["listing"]