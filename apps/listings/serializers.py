from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils import timezone
from apps.commons.models import Tag

from apps.mixins import constants
from apps.properties import serializers as prop_serializers

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


class BaseListingSerializer(ModelSerializer):
    listing_type_data = serializers.SerializerMethodField(read_only=True)
    is_expired = serializers.SerializerMethodField(read_only=True)
    is_approved = serializers.SerializerMethodField(read_only=True)
    is_featuring_approved = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)
    tags = serializers.SerializerMethodField(read_only=True)
    unit_type = serializers.SerializerMethodField(read_only=True)
    property_category = serializers.CharField(
        read_only=True, source="main_property.property_category.cat_key"
    )
    # main_property = prop_serializers.PropertyAnySerializer(read_only=True)

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
            "unit_type",
            "tags",
            "agent_branch",
            "agent",
            "main_property",
            "property_category",
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
            "listing_payment_type",
        ]

    def get_listing_type_data(self, obj):
        """
        Get Rend or Sale related data
        """
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

    def get_unit_type(self, obj):
        if hasattr(obj, "officelisting"):
            return constants.LISTING_PROPERTY_UNIT_TYPE_OFFICE_UNIT
        elif hasattr(obj, "othercommercialpropertyunitlisting"):
            return constants.LISTING_PROPERTY_UNIT_TYPE_OTHER_COMMERCIAL_PROPERTY_UNIT
        elif hasattr(obj, "apartmentunitlisting"):
            return constants.LISTING_PROPERTY_UNIT_TYPE_APARTMENT_UNIT
        else:
            return ""

    def get_tags(self, obj):
        # GET TAGS THAT CAN BE APPLIED TO LISTING
        tags = Tag.objects.filter(apply_to=constants.TAG_APPLY_TO_LISTING)

        # LOCAL VARIABLES TO BE PASSED TO EXEC FUNCTION
        locals = {"listing": obj, "timezone": timezone}

        # LISTING TAGS THAT CAN BE ATTACHED TO THE LISTING
        listing_tags = []

        # GET THE RESULT FROM LOCALS NAMESPACE FOR EACH TAG. THE RESULT OF
        # THE CONDITION WILL BE BOOLEAN
        for tag in tags:
            exec(tag.condition_code, locals)
            if locals["result"]:
                listing_tags.append(tag.name)
        return listing_tags


class ListingSerializer(BaseListingSerializer):
    class Meta:
        model = listing_models.Listing
        fields = BaseListingSerializer.Meta.fields
        read_only_fields = BaseListingSerializer.Meta.read_only_fields


class ListingListSerializer(BaseListingSerializer):
    main_property = prop_serializers.ListingPropertySerializer(read_only=True)

    class Meta:
        model = listing_models.Listing
        fields = BaseListingSerializer.Meta.fields + ["main_property"]
        read_only_fields = BaseListingSerializer.Meta.read_only_fields


class ApartmentUnitListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.ApartmentUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class ApartmentUnitListingForListingDetailSerializer(ModelSerializer):
    apartment_unit = prop_serializers.ApartmentUnitSerializer(read_only=True)
    apartment = prop_serializers.ApartmentWithoutUnitsSerializer(read_only=True)

    class Meta:
        model = listing_models.ApartmentUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class CondominiumListingForListingDetailSerializer(ModelSerializer):
    condominium = prop_serializers.CondominiumSerializer(read_only=True)

    class Meta:
        model = listing_models.CondominiumListing
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


class VillaListingForListingDetailSerializer(ModelSerializer):
    villa = prop_serializers.VillaSerializer(read_only=True)

    class Meta:
        model = listing_models.VillaListing
        fields = "__all__"
        read_only_fields = ["listing"]


class TownhouseListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.TownhouseListing
        fields = "__all__"
        read_only_fields = ["listing"]


class TownhouseListingForListingDetailSerializer(ModelSerializer):
    townhouse = prop_serializers.TownhouseSerializer(read_only=True)

    class Meta:
        model = listing_models.TownhouseListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SharehouseListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.SharehouseListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SharehouseListingForListingDetailSerializer(ModelSerializer):
    sharehouse = prop_serializers.SharehouseSerializer(read_only=True)

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


class VenueListingForListingDetailSerializer(ModelSerializer):
    venue = prop_serializers.VenueSerializer(read_only=True)

    class Meta:
        model = listing_models.VenueListing
        fields = "__all__"
        read_only_fields = ["listing"]


class LandListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.LandListing
        fields = "__all__"
        read_only_fields = ["listing"]


class LandListingForListingDetailSerializer(ModelSerializer):
    land = prop_serializers.LandSerializer(read_only=True)

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


class OfficeUnitListingForListingDetailSerializer(ModelSerializer):
    office_unit = prop_serializers.OfficeUnitSerializer(read_only=True)
    commercial_property = prop_serializers.CommercialPropertyWithoutUnitsSerializer(
        read_only=True
    )

    class Meta:
        model = listing_models.OfficeListing
        fields = "__all__"
        read_only_fields = ["listing"]


class OtherCommercialPropertyUnitListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.OtherCommercialPropertyUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class OtherCommercialPropertyUnitListingForListingDetailSerializer(ModelSerializer):
    other_commercial_property_unit = (
        prop_serializers.OtherCommercialPropertyUnitSerializer(read_only=True)
    )
    commercial_property = prop_serializers.CommercialPropertyWithoutUnitsSerializer(
        read_only=True
    )

    class Meta:
        model = listing_models.OtherCommercialPropertyUnitListing
        fields = "__all__"
        read_only_fields = ["listing"]


class SavedListingSerializer(ModelSerializer):
    class Meta:
        model = listing_models.SavedListing
        fields = "__all__"
        read_only_fields = ["listing"]


class ListingDetailSerializer(BaseListingSerializer):
    sub_property_listing = serializers.SerializerMethodField(read_only=True)
    main_property = prop_serializers.ListingPropertySerializer(read_only=True)

    class Meta:
        model = listing_models.Listing
        fields = BaseListingSerializer.Meta.fields + [
            "sub_property_listing",
            "main_property",
        ]
        read_only_fields = BaseListingSerializer.Meta.read_only_fields

    def get_sub_property_listing(self, obj):
        property_category_key = obj.main_property.property_category.cat_key

        if property_category_key == constants.APARTMENT_KEY:
            return ApartmentUnitListingForListingDetailSerializer(
                instance=listing_models.ApartmentUnitListing.objects.get(listing=obj.id)
            ).data
        elif property_category_key == constants.VILLA_KEY:
            return VillaListingForListingDetailSerializer(
                instance=listing_models.VillaListing.objects.get(listing=obj.id)
            ).data
        elif property_category_key == constants.CONDOMINIUM_KEY:
            return CondominiumListingForListingDetailSerializer(
                instance=listing_models.CondominiumListing.objects.get(listing=obj.id)
            ).data
        elif property_category_key == constants.SHAREHOUSE_KEY:
            return SharehouseListingForListingDetailSerializer(
                instance=listing_models.SharehouseListing.objects.get(listing=obj.id)
            ).data
        elif property_category_key == constants.TOWNHOUSE_KEY:
            return TownhouseListingForListingDetailSerializer(
                instance=listing_models.TownhouseListing.objects.get(listing=obj.id)
            ).data
        elif property_category_key == constants.COMMERCIAL_PROPERTY_KEY:
            office_unit = listing_models.OfficeListing.objects.filter(listing=obj.id)
            if office_unit.exists():
                return OfficeUnitListingForListingDetailSerializer(
                    instance=office_unit.first()
                ).data

            other_unit = (
                listing_models.OtherCommercialPropertyUnitListing.objects.filter(
                    listing=obj.id
                )
            )

            if other_unit.exists():
                return OtherCommercialPropertyUnitListingForListingDetailSerializer(
                    instance=other_unit.first()
                ).data
