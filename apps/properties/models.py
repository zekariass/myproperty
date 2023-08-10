from ast import Set
import re
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.agents import models as agnt_models
from apps.commons import models as cmn_models
from apps.properties.tasks import send_new_property_added_email_to_agent
from apps.system import models as sys_models
from apps.mixins.common_fields import (
    AddedOnFieldMixin,
    DescriptionAndAddedOnFieldMixin,
    ExpireOnFieldMixin,
    PropertyStatusFieldMixin,
    CommonResidentialFieldsMixin,
    CommonPropertyShallowFieldsMixin,
)
from apps.mixins.functions import (
    property_plan_upload_path,
    property_image_path,
    property_video_path,
)
from apps.mixins import constants


class AmenityCategory(DescriptionAndAddedOnFieldMixin):
    """
    The amenity category is a category of amenities that a property may have,
    such as entertainment, cleaning, kitchen, etc
    """

    name = models.CharField(
        verbose_name="amenity category name", max_length=150, unique=True
    )

    def __str__(self):
        return f"{self.name}"


class Amenity(DescriptionAndAddedOnFieldMixin):
    """Amenity is an important feature of a property that the buyer or tenant may like to have with the property"""

    category = models.ForeignKey(
        AmenityCategory,
        related_name="amenities",
        related_query_name="amenity",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="amenity name",
        max_length=100,
        unique=True,
        blank=False,
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["id", "category"], name="unique-amenity-category-constriant"
            )
        ]

    def __str__(self):
        return f"{self.id} {self.name}"


class PropertyCategory(DescriptionAndAddedOnFieldMixin):
    """Each property has category"""

    name = models.CharField(
        verbose_name="property category name",
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )
    cat_key = models.CharField(
        verbose_name="property category key",
        max_length=10,
        choices=constants.PROPERTY_CATEGORY_KEY,
        unique=True,
    )
    amenities = models.ManyToManyField(
        Amenity,
        related_name="property_categories",
        related_query_name="property_category",
        through="PropertyCategoryAmenity",
        blank=True,
    )

    def __str__(self):
        return f"{self.id} {self.name}"

    def save(self, *args, **kwargs):
        category_keys = [key for key, _ in constants.PROPERTY_CATEGORY_KEY]

        if not self.cat_key in category_keys:
            raise ValueError({"category_key": "Invalid Category Key"})

        super().save(*args, **kwargs)


class PropertyCategoryAmenity(AddedOnFieldMixin):
    """Property Category and Amenity intermediate table"""

    property_category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property_category", "amenity"],
                name="prop_cat_amenity_unique_constraint",
            )
        ]

    def __str__(self):
        return f"{self.property_category.name}, {self.amenity.name}"


class Property(DescriptionAndAddedOnFieldMixin):
    """Property is parent class of all property categories"""

    custom_prop_id = models.CharField("custom property id", max_length=15, unique=True)
    property_category = models.ForeignKey(
        PropertyCategory, on_delete=models.CASCADE, related_name="category_properties"
    )
    agent_branch = models.ForeignKey(
        agnt_models.AgentBranch,
        on_delete=models.CASCADE,
        related_name="branch_properties",
        related_query_name="branch_property",
        verbose_name="property agent branch",
    )
    agent = models.ForeignKey(
        agnt_models.Agent,
        on_delete=models.CASCADE,
        related_name="agent_properties",
        related_query_name="agent_property",
        verbose_name="property agent",
    )
    address = models.OneToOneField(
        cmn_models.Address,
        on_delete=models.SET_NULL,
        related_name="address_properties",
        related_query_name="address_property",
        verbose_name="property address",
        null=True,
    )
    name = models.CharField(
        "Prperty name or label", max_length=150, blank=True, null=True
    )
    is_residential = models.BooleanField(
        verbose_name="is property for residence?", default=True
    )
    tenure = models.CharField(max_length=100, choices=constants.PROPERTY_TENURE_TYPES)
    tax_band = models.CharField(max_length=50, choices=constants.PROPERTY_TAX_BANDS)
    amenity = models.ManyToManyField(
        Amenity,
        related_name="amenity_properties",
        related_query_name="amenity_property",
        through="PropertyAmenity",
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "agent"],
                name="unique_property_name_in_an_agent_constraint",
                condition=models.Q(name__isnull=False),
                violation_error_message="A property should have a unique name within the property. [name, agent] duplicate.",
            )
        ]

    @property
    def cat_key(self):
        return self.property_category.cat_key

    # @property
    # def agent(self):
    #     return self.agent_branch.agent

    def save(self, *args, **kwargs):
        self.agent = self.agent_branch.agent
        super().save(*args, **kwargs)

    def __str__(self):
        return "%d %s" % (self.pk, self.property_category.name)


class PropertyAmenity(AddedOnFieldMixin):
    """Intermediary table between Property and Amenity"""

    parent_property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent_property", "amenity"],
                name="property_amenity_unique_constraint",
            )
        ]

    def __str__(self) -> str:
        return f"{self.parent_property.custom_prop_id, self.amenity.name}"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print("=====================================>: ", kwargs)

    # def save(self, *args, **kwargs):
    #     property_category = self.parent_property.property_category
    #     priperty_category_amenities = PropertyCategoryAmenity.objects.filter(
    #         property_category=property_category
    #     )


class Apartment(AddedOnFieldMixin, PropertyStatusFieldMixin):
    """Apartment"""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="apartment",
    )
    floors = models.PositiveIntegerField(
        verbose_name="number of floors in the building", default=0
    )
    # is_multi_unit = models.BooleanField(
    #     verbose_name='is multi unit?', default=False)
    # agent = models.BigIntegerField(verbose_name='agent who creates the apartment', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     self.agent = self.property.agent.id
    #     super(Apartment, self).save(*args, **kwargs)

    def is_multi_unit(self):
        return self.apartment_units.all().count() > 1

    def __str__(self):
        return f"Apartment {self.id}: {self.floors} floors"


class PropertyPlan(AddedOnFieldMixin, CommonPropertyShallowFieldsMixin):
    """A plan map or blueprint of the proproperty rooms"""

    parent_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_plans",
        related_query_name="property_plan",
    )
    label = models.CharField("plan label", max_length=100, null=True, blank=True)
    file_path = models.ImageField("plan label", upload_to=property_plan_upload_path)
    file_ext = models.CharField("file extension", max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        ext_pattern = "((\.[A-z]+))"
        ext = re.search(ext_pattern, self.file_path)
        self.file_ext = ext.group(1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file_path}"


class ApartmentUnit(CommonResidentialFieldsMixin, AddedOnFieldMixin):
    """An apartment will have at lest one unit"""

    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        verbose_name="main apartment",
        related_name="apartment_units",
        related_query_name="apartment_unit",
    )
    unit_name_or_number = models.CharField(max_length=100)
    property_plan = models.OneToOneField(
        PropertyPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Plan image for this unit",
    )

    # Disable status from being inherited from abstract common fields
    status = None

    def __str__(self) -> str:
        return f"Apartment Unit: {self.id} {self.unit_name_or_number}"


class ApartmentUnitAmenity(AddedOnFieldMixin):
    apartment_unit = models.ForeignKey(ApartmentUnit, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["apartment_unit", "amenity"],
                name="apartment_unit_amenity_unique_constraint",
            )
        ]

    def __str__(self):
        return (
            f"{self.id} {self.apartment_unit.unit_name_or_number} {self.amenity.name}"
        )


class Condominium(
    CommonResidentialFieldsMixin, AddedOnFieldMixin, CommonPropertyShallowFieldsMixin
):
    """Condominiums are similar of apartment where parts of the property is owned by many residents"""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="condominium",
    )
    # @property
    # def agent(self):
    #     return f"{self.parent_property.agent_branch.agent}"

    # @property
    # def agent_branch(self):
    #     return f"{self.parent_property.agent_branch}"

    # @property
    # def cat_key(self):
    #     return f"{self.parent_property.cat_key}"

    def __str__(self):
        return "Condominium: %s bath rooms and %s bed rooms" % (
            self.bath_rooms,
            self.bed_rooms,
        )


class Villa(
    CommonResidentialFieldsMixin, AddedOnFieldMixin, CommonPropertyShallowFieldsMixin
):
    """A villa is a large, detached structure with spacious land surrounding it. It is very luxurious and
    may include amenities such as a pool, stables, and gardens. A villa is generally home to a single-family,
    in contrast to condos and townhomes that are designed to house multiple families."""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="villa",
    )
    total_compound_area = models.FloatField(default=0.00)
    housing_area = models.FloatField(default=0.00)
    floors = models.IntegerField(
        "number of fields", default=1, validators=[MinValueValidator(0)]
    )
    # Disable area from being inherited from abstract common fields
    area = None
    floor = None

    def __str__(self):
        return "Villa: %s bath rooms and %s bed rooms" % (
            self.bath_rooms,
            self.bed_rooms,
        )


class Townhouse(
    CommonResidentialFieldsMixin, AddedOnFieldMixin, CommonPropertyShallowFieldsMixin
):
    """Town house is a property type which is common in cities and towns"""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="townhouse",
    )
    structure = models.CharField(
        "property structure", choices=constants.PROPERTY_STRUCTURE, max_length=100
    )

    def __str__(self):
        return "Townhouse: %s bath rooms and %s bed rooms" % (
            self.bath_rooms,
            self.bed_rooms,
        )


class BuildingType(DescriptionAndAddedOnFieldMixin):
    """Building type, such as Apartment, Condominium, Traditional House, etc"""

    type = models.CharField(
        max_length=100, choices=constants.BUILDING_TYPES, unique=True
    )

    def __str__(self):
        return f"{self.id} {self.type}"


"""Share House is a house that someone may share it with someone else"""


class Sharehouse(AddedOnFieldMixin, CommonPropertyShallowFieldsMixin):
    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="sharehouse",
    )
    building_type = models.ForeignKey(
        BuildingType,
        related_name="building_types",
        related_query_name="building_type",
        verbose_name="building type",
        on_delete=models.SET_NULL,
        null=True,
    )
    floor = models.IntegerField(verbose_name="Home floor level", default=0)
    total_area = models.FloatField(default=0.00)
    shared_rooms_furnished = models.BooleanField(
        verbose_name="is the home furnished?", default=False
    )
    status = models.CharField(
        "current status of the property",
        choices=constants.PROPERTY_STATUS,
        max_length=50,
    )
    structure = models.CharField(
        "property structure", choices=constants.PROPERTY_STRUCTURE, max_length=100
    )

    def __str__(self) -> str:
        return f"Sharehouse: uilding type {self.building_type}"


class Room(AddedOnFieldMixin, CommonResidentialFieldsMixin):
    "Sharehouse rooms"
    sharehouse = models.ForeignKey(
        Sharehouse,
        on_delete=models.CASCADE,
        related_name="rooms",
        related_query_name="room",
    )
    has_ensuite_bathroom = models.BooleanField(
        "does the room has ensuite bathroom?", default=False
    )
    for_gender = models.CharField(
        "required of gender of new flatmate", choices=constants.GENDER, max_length=30
    )
    for_speaker_of_languages = models.CharField(
        "speaker of language needed", max_length=100, null=True, blank=True
    )
    flatmate_interests = models.CharField(
        "what interests new flatmate expected to have?",
        max_length=200,
        null=True,
        blank=True,
    )
    occupied = models.BooleanField("is the room occupied?", default=False)
    status = None
    bath_rooms = None

    def __str__(self):
        languages = self.for_speaker_of_languages or "Any"
        return f"Sharehouse Room: for gender: {self.for_gender.title()}  and speaker of: {languages.title()}"


class CommercialProperty(
    AddedOnFieldMixin,
    #  CommonResidentialFieldsMixin,
    CommonPropertyShallowFieldsMixin,
):
    """Commercial property is a property that is used for commercial or trading purposes"""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="commercial_property",
    )
    unit_type = models.CharField(
        "commercial property unit type",
        max_length=20,
        choices=constants.COMMERCIAL_PROPERTY_UNIT_TYPES,
    )
    has_parking_space = models.BooleanField(
        verbose_name="is the commercial property new?", default=False
    )
    floors = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # is_multi_unit = models.BooleanField(default=False, blank=True)
    status = models.CharField(
        "current status of the property",
        choices=constants.PROPERTY_STATUS,
        max_length=50,
    )
    bath_rooms = None
    bed_rooms = None

    @property
    def is_multi_unit(self):
        return (self.other_units.all().count() + self.office_units.all().count()) > 1

    def __str__(self) -> str:
        return f"Commercial Property: {self.floors} floors"


class OfficeUnit(DescriptionAndAddedOnFieldMixin, CommonResidentialFieldsMixin):
    """The office is a commercial property that is used for office purposes"""

    commercial_property = models.ForeignKey(
        CommercialProperty,
        on_delete=models.CASCADE,
        verbose_name="parent commercial property",
        related_name="office_units",
        related_query_name="office_unit",
    )
    unit_name_or_number = models.CharField(max_length=100)
    seats = models.PositiveIntegerField(
        "number of seats the office is enough for?", default=1
    )
    rooms = models.PositiveIntegerField("number of rooms in the office?", default=1)
    property_plan = models.OneToOneField(
        PropertyPlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    bath_rooms = None
    bed_rooms = None
    status = None

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["commercial_property", "unit_name_or_number"],
                name="unique_office_unit_in_single_commercial_property_constraint",
            )
        ]

    def __str__(self):
        return f"Office: {self.seats} seats"


class OfficeUnitAmenity(AddedOnFieldMixin):
    """Association class between OfficeUnit and Ammenity"""

    office_unit = models.ForeignKey(OfficeUnit, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["office_unit", "amenity"],
                name="office_unit_amenity_constraint",
            )
        ]


class OtherCommercialPropertyUnit(
    DescriptionAndAddedOnFieldMixin, CommonResidentialFieldsMixin
):
    """Commercial properties may have multiple units.
    Units are a part of the property to be rented or sold independently.
    For instance, a commercial centre may be registered as one commercial
    property and it then has different units"""

    commercial_property = models.ForeignKey(
        CommercialProperty,
        on_delete=models.CASCADE,
        verbose_name="parent commercial property",
        related_name="other_units",
        related_query_name="other_unit",
    )
    unit_name_or_number = models.CharField(max_length=100)
    rooms = models.PositiveIntegerField("number of rooms in the unit?", default=1)
    property_plan = models.OneToOneField(
        PropertyPlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    amenities = models.ManyToManyField(
        Amenity, through="OtherCommercialPropertyUnitAmenity"
    )
    bath_rooms = None
    bed_rooms = None
    status = None
    is_furnished = None

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["commercial_property", "unit_name_or_number"],
                name="unique_other_unit_in_single_commercial_property_constraint",
            )
        ]

    def __str__(self):
        return f"Other Commercial Property Unit: Id: {self.id} with {self.rooms} rooms"


class OtherCommercialPropertyUnitAmenity(AddedOnFieldMixin):
    """Association class between OtherCommercialPropertyUnit and Ammenity"""

    other_commercial_property_unit = models.ForeignKey(
        OtherCommercialPropertyUnit, on_delete=models.CASCADE
    )
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["other_commercial_property_unit", "amenity"],
                name="other_commercial_property_unit_amenity_constraint",
            )
        ]


"""Hall is a wide room used for meetings and various ceremonies"""


class Venue(AddedOnFieldMixin, CommonPropertyShallowFieldsMixin):
    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="venue",
    )
    seat_capacity = models.PositiveIntegerField(
        "how many seats the venue has?", default=5
    )
    total_capacity = models.PositiveIntegerField(
        "total capacity including standing", default=5
    )
    area = models.DecimalField("venue area", max_digits=12, decimal_places=5)

    def __str__(self):
        return f"Hall: with {self.total_capacity} capacity"


class LandType(DescriptionAndAddedOnFieldMixin):
    name = models.CharField("land type name", max_length=100, unique=True)

    def __str__(self) -> str:
        return f"Land Type: {self.id} {self.name}"


class Land(AddedOnFieldMixin, CommonPropertyShallowFieldsMixin):
    """Land properties"""

    parent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        verbose_name="main property",
        related_name="land",
    )
    land_type = models.ForeignKey(
        LandType,
        on_delete=models.CASCADE,
        related_name="lands",
        related_query_name="land",
        null=True,
        blank=True,
    )
    area = models.FloatField(verbose_name="area of the land", default=0.00)

    def __str__(self):
        return "%s area land" % (self.area)


class PropertyImageLabel(DescriptionAndAddedOnFieldMixin):
    """This is the image identifier uploaded to the image"""

    name = models.CharField("image label name", max_length=100, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class PropertyImage(AddedOnFieldMixin):
    """Images of a property. A property may have one or more images uploaded"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_images",
        related_query_name="property_image",
    )
    file_path = models.ImageField("property image", upload_to=property_image_path)
    file_ext = models.CharField("file extension", max_length=10, null=True, blank=True)
    label = models.ForeignKey(
        PropertyImageLabel,
        related_name="label_images",
        related_query_name="label_image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        pattern = "(\.[A-z]+$)"
        ext = re.search(pattern, self.file_path.url)
        self.file_ext = ext.group(1)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.file_path}"


class PropertyVideo(AddedOnFieldMixin):
    """Images of a property. A property may have one or more images uploaded"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_videos",
        related_query_name="property_video",
    )
    file_path = models.FileField("property video", upload_to=property_video_path)
    file_ext = models.CharField("file extension", max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        pattern = "(\.[A-z]+)"
        ext = re.search(pattern, self.file_path)
        self.file_ext = ext.group(1)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.file_path}"


class PropertyKeyFeature(DescriptionAndAddedOnFieldMixin):
    """Property key features. Addtional features that the agent wish to add"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="key_features",
        related_query_name="key_feature",
    )
    name = models.CharField("feature name", max_length=150)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property", "name"],
                name="property_unique_feature_name_constraint",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class ListingPriceByPropertyCategory(
    DescriptionAndAddedOnFieldMixin,  # ExpireOnFieldMixin
):
    """Every category may have a different listing price set by administrators"""

    property_category = models.ForeignKey(
        PropertyCategory,
        related_name="listing_price_by_property_category",
        on_delete=models.CASCADE,
    )
    listing_type = models.CharField(max_length=20, choices=constants.LISTING_TYPE)
    price_percentage = models.DecimalField(
        help_text="Percentage value of the property price that the agent should pay for listing",
        decimal_places=5,
        max_digits=10,
        default=0.00000,
    )
    price_fixed = models.DecimalField(
        help_text="Fixed value that the agent should pay for listing",
        decimal_places=5,
        max_digits=10,
        default=0.00000,
    )
    price_lower_bound = models.DecimalField(
        help_text="minimum listing price",
        decimal_places=5,
        max_digits=10,
        default=0.00000,
    )
    price_upper_bound = models.DecimalField(
        help_text="maximum listing price",
        decimal_places=5,
        max_digits=10,
        default=0.00000,
    )
    # currency = models.ForeignKey(
    #     sys_models.Currency, on_delete=models.SET_NULL, blank=True, null=True
    # )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property_category", "listing_type"],
                name="single_listing_price_by_property_category_constraint",
            )
        ]

    # @property
    # def is_expired(self):
    #     expired = self.expire_on >= timezone.now
    #     return expired

    # def save(self, *args, **kwargs):
    #     # Check if this instance is unexpired and there is unexpired instance already
    #     unexpired_listing_price_exist = (
    #         self.expire_on >= timezone.now()
    #     ) and ListingPriceByPropertyCategory.objects.filter(
    #         expire_on__gte=timezone.now(),
    #         property_category=self.property_category,
    #         listing_type=self.listing_type,
    #     ).exclude(
    #         id=self.id
    #     ).exists()

    #     if unexpired_listing_price_exist:
    #         raise IntegrityError(
    #             f"Active listing price for listing type: {self.listing_type} and property category: {self.property_category.name} exists"
    #         )

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Listing Price: {self.property_category.name}, {self.listing_type}"


class ListingPriceByPropertyCategoryHistory(
    DescriptionAndAddedOnFieldMixin,  # ExpireOnFieldMixin
):
    """Every category may have a different listing price set by administrators"""

    property_category = models.ForeignKey(
        PropertyCategory,
        related_name="listing_price_by_property_category_history",
        on_delete=models.CASCADE,
    )
    listing_type = models.CharField(max_length=20)
    price_percentage = models.DecimalField(
        help_text="Percentage value of the property price that the agent should pay for listing",
        decimal_places=5,
        max_digits=10,
    )
    price_fixed = models.DecimalField(
        help_text="Fixed value that the agent should pay for listing",
        decimal_places=5,
        max_digits=10,
    )
    price_lower_bound = models.DecimalField(
        help_text="minimum listing price", decimal_places=5, max_digits=10
    )
    price_upper_bound = models.DecimalField(
        help_text="maximum listing price", decimal_places=5, max_digits=10
    )
    currency = models.ForeignKey(
        sys_models.Currency, on_delete=models.SET_NULL, blank=True, null=True
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["property_category", "listing_type"],
    #             name="single_listing_price_by_property_category_history_constraint",
    #         )
    #     ]

    # @property
    # def is_expired(self):
    #     expired = self.expire_on >= timezone.now
    #     return expired

    def __str__(self):
        return f"Listing Price: {self.property_category.name}, {self.listing_type}"
