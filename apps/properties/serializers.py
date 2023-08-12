from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models as prop_models

from apps.commons.serializers import AddressSerializer
from apps.agents import serializers as agent_serializers
from apps.mixins import constants


class AmenityCategorySerializer(ModelSerializer):
    class Meta:
        model = prop_models.AmenityCategory
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.Amenity
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class PropertyCategorySerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyCategory
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class ListingPriceByPropertyCategorySerializer(ModelSerializer):
    class Meta:
        model = prop_models.ListingPriceByPropertyCategory
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class BuildingTypeSerializer(ModelSerializer):
    class Meta:
        model = prop_models.BuildingType
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class LandTypeSerializer(ModelSerializer):
    class Meta:
        model = prop_models.LandType
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class PropertyKeyFeatureSerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyKeyFeature
        fields = "__all__"
        read_only_fields = ["id", "added_on", "property"]


class PropertyImageLabelSerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyImageLabel
        fields = "__all__"
        read_only_fields = ["id", "added_on"]


class PropertyImageSerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyImage
        fields = "__all__"
        read_only_fields = ["id", "added_on", "property"]


class PropertyVideoSerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyVideo
        fields = "__all__"
        read_only_fields = ["id", "added_on", "property"]


class PropertyPlanSerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyPlan
        fields = "__all__"
        read_only_fields = ["id", "added_on", "property"]


class ApartmentUnitSerializer(ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnit
        fields = [
            "id",
            "unit_name_or_number",
            "bed_rooms",
            "bath_rooms",
            "area",
            "is_furnished",
            "floor",
            "added_on",
            "apartment",
            "property_plan",
        ]
        read_only_fields = ["id", "apartment", "added_on"]


class ApartmentSerializer(ModelSerializer):
    units = ApartmentUnitSerializer(read_only=True, source="apartment_units", many=True)

    class Meta:
        model = prop_models.Apartment
        fields = [
            "id",
            "floors",
            "status",
            "is_multi_unit",
            "added_on",
            "parent_property",
            "units",
        ]
        read_only_fields = ["id", "parent_property", "added_on"]


class SharehouseRoomSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Room
        fields = [
            "id",
            "has_ensuite_bathroom",
            "floor",
            "bed_rooms",
            "is_furnished",
            "area",
            "for_gender",
            "for_speaker_of_languages",
            "flatmate_interests",
            "occupied",
            "sharehouse",
            "added_on",
        ]
        read_only_fields = ["id", "sharehouse", "added_on"]


class SharehouseSerializer(ModelSerializer):
    # building_type = BuildingTypeSerializer()
    units = SharehouseRoomSerializer(read_only=True, source="rooms", many=True)

    class Meta:
        model = prop_models.Sharehouse
        fields = [
            "id",
            "total_area",
            "shared_rooms_furnished",
            "status",
            "structure",
            "building_type",
            "added_on",
            "parent_property",
            "units",
        ]
        read_only_fields = ["id", "parent_property", "units", "added_on"]

    # def get_units(self, instance):
    #     return SharehouseRoomSerializer(instance)


class CondominiumSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Condominium
        fields = [
            "id",
            "floor",
            "bath_rooms",
            "bed_rooms",
            "area",
            "is_furnished",
            "status",
            "area",
            "parent_property",
            "added_on",
        ]
        read_only_fields = ["id", "parent_property", "added_on"]


class VillaSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Villa
        fields = [
            "id",
            "floors",
            "bath_rooms",
            "bed_rooms",
            "housing_area",
            "total_compound_area",
            "is_furnished",
            "status",
            "parent_property",
            "added_on",
        ]
        read_only_fields = ["id", "parent_property", "added_on"]


class TownhouseSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Townhouse
        fields = [
            "id",
            "floor",
            "bath_rooms",
            "bed_rooms",
            "area",
            "is_furnished",
            "status",
            "area",
            "parent_property",
            "structure",
            "added_on",
        ]
        read_only_fields = ["id", "parent_property", "added_on"]


class OfficeUnitSerializer(ModelSerializer):
    class Meta:
        model = prop_models.OfficeUnit
        fields = [
            "id",
            "commercial_property",
            "unit_name_or_number",
            "seats",
            "rooms",
            "area",
            "property_plan",
            "added_on",
        ]
        read_only_fields = ["id", "commercial_property", "added_on"]


class OtherCommercialPropertyUnitSerializer(ModelSerializer):
    class Meta:
        model = prop_models.OtherCommercialPropertyUnit
        fields = [
            "id",
            "commercial_property",
            "unit_name_or_number",
            "rooms",
            "area",
            "description",
            "property_plan",
            "amenities",
            "added_on",
        ]
        read_only_fields = ["id", "commercial_property", "added_on"]


class CommercialPropertySerializer(ModelSerializer):
    is_multi_unit = serializers.SerializerMethodField()
    units = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = prop_models.CommercialProperty
        fields = [
            "id",
            "floors",
            "status",
            "is_multi_unit",
            "units",
            "added_on",
        ]
        read_only_fields = ["id", "is_multi_unit", "added_on"]

    def get_is_multi_unit(self, instance):
        return instance.is_multi_unit

    def get_units(self, instance):
        return {
            "office_units": OfficeUnitSerializer(
                instance=instance.office_units, many=True
            ).data,
            "other_units": OtherCommercialPropertyUnitSerializer(
                instance=instance.other_units, many=True
            ).data,
        }


# class CommercialPropertySerializer(ModelSerializer):
#     class Meta:
#         model = prop_models.CommercialProperty
#         fields = "__all__"


class VenueSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Venue
        fields = [
            "id",
            "seat_capacity",
            "total_capacity",
            "area",
            "parent_property",
            "added_on",
        ]
        read_only_fields = ["id", "parent_property", "added_on"]


class LandSerializer(ModelSerializer):
    class Meta:
        model = prop_models.Land
        fields = ["id", "area", "land_type", "parent_property", "added_on"]
        read_only_fields = ["id", "parent_property", "added_on"]


class PropertyCreateSerializer(ModelSerializer):
    # sub_property = serializers.SerializerMethodField()
    # property_category = PropertyCategorySerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    # agent = serializers.IntegerField(source="agent_branch.agent")

    class Meta:
        model = prop_models.Property
        fields = [
            "id",
            "custom_prop_id",
            "property_category",
            "name",
            "is_residential",
            "tenure",
            "tax_band",
            "description",
            "added_on",
            "agent",
            "agent_branch",
            "address",
        ]
        read_only_fields = [
            "id",
            "custom_prop_id",
            "is_residential",
            "address",
            "agent",
            "added_on",
        ]


# class PropertyUpdateSerializer(ModelSerializer):
#     """Serialiser for operation other than create"""

#     property_category = PropertyCategorySerializer(read_only=True)

#     class Meta:
#         model = prop_models.Property
#         fields = [
#             "id",
#             "custom_prop_id",
#             "property_category",
#             "name",
#             "is_residential",
#             "tenure",
#             "tax_band",
#             "description",
#             "added_on",
#         ]

#         read_only_fields = ["id", "added_on"]


class PropertyAnySerializer(ModelSerializer):
    """Serialiser for operation other than create"""

    sub_property = serializers.SerializerMethodField()
    property_category = PropertyCategorySerializer(read_only=True)

    class Meta:
        model = prop_models.Property
        fields = [
            "id",
            "custom_prop_id",
            "property_category",
            "name",
            "agent",
            "is_residential",
            "tenure",
            "tax_band",
            "description",
            "added_on",
            "sub_property",
        ]

        read_only_fields = ["id", "custom_prop_id", "added_on"]

    def get_sub_property(self, instance):
        if instance.cat_key == constants.APARTMENT_KEY:
            return ApartmentSerializer(instance=instance.apartment).data
        elif instance.cat_key == constants.CONDOMINIUM_KEY:
            return CondominiumSerializer(instance=instance.condominium).data
        elif instance.cat_key == constants.SHAREHOUSE_KEY:
            return SharehouseSerializer(instance=instance.sharehouse).data
        elif instance.cat_key == constants.VILLA_KEY:
            return VillaSerializer(instance=instance.villa).data
        elif instance.cat_key == constants.TOWNHOUSE_KEY:
            return TownhouseSerializer(instance=instance.townhouse).data
        elif instance.cat_key == constants.COMMERCIAL_PROPERTY_KEY:
            return CommercialPropertySerializer(
                instance=instance.commercial_property
            ).data
        elif instance.cat_key == constants.VENUE_KEY:
            return VenueSerializer(instance=instance.venue).data
        elif instance.cat_key == constants.LAND_KEY:
            return LandSerializer(instance=instance.land).data

    # @property
    # def data(self):
    #     data = super().data
    #     child_serializer = self.get_child_property(self.instance)
    #     if child_serializer:
    #         data["sub_property"] = child_serializer.data
    #     return data


class PropertyCategoryAmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyCategoryAmenity
        fields = "__all__"
        read_only_fields = ["id", "added_on", "property_category"]


class PropertyAmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.PropertyAmenity
        fields = "__all__"
        read_only_fields = ["id", "added_on", "parent_property"]


class ApartmentUnitAmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.ApartmentUnitAmenity
        fields = "__all__"
        read_only_fields = ["id", "added_on", "apartment_unit"]


class OfficeUnitAmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.OfficeUnitAmenity
        fields = "__all__"
        read_only_fields = ["id", "added_on", "office_unit"]


class OtherCommercialPropertyUnitAmenitySerializer(ModelSerializer):
    class Meta:
        model = prop_models.OtherCommercialPropertyUnitAmenity
        fields = "__all__"
        read_only_fields = ["id", "added_on", "other_commercial_property_unit"]
