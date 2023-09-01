from django.urls import path

from . import views as prop_views

urlpatterns = [
    # ======================================================================
    # AMENITY CATEGORY ROUTES
    # ======================================================================
    path(
        "amenities/categories/",
        prop_views.AmenityCategoryListCreateView.as_view(),
        name="list-create-amenity-category",
    ),
    path(
        "amenities/categories/<int:pk>/",
        prop_views.AmenityCategoryRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-amenity-category",
    ),
    # ======================================================================
    # AMENITY ROUTES
    # ======================================================================
    path(
        "amenities/",
        prop_views.AmenityListCreateView.as_view(),
        name="list-create-amenity",
    ),
    path(
        "amenities/<int:pk>/",
        prop_views.AmenityRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-amenity",
    ),
    # ======================================================================
    # PROPERTY CATEGORY ROUTES
    # ======================================================================
    path(
        "categories/",
        prop_views.PropertyCategoryListCreateView.as_view(),
        name="list-create-property-category",
    ),
    path(
        "categories/<int:pk>/",
        prop_views.PropertyCategoryRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-category",
    ),
    # ======================================================================
    # LISTING PRICE BY PROPERTY CATEGORY ROUTES
    # ======================================================================
    path(
        "listing-price-by-property-categories/",
        prop_views.ListingPriceByPropertyCategoryListCreateView.as_view(),
        name="list-create-listing-price-by-property-category",
    ),
    path(
        "listing-price-by-property-categories/<int:pk>/",
        prop_views.ListingPriceByPropertyCategoryRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-listing-price-by-property-category",
    ),
    # ======================================================================
    # BUILDING TYPE ROUTES
    # ======================================================================
    path(
        "building-types/",
        prop_views.BuildingTypeListCreateView.as_view(),
        name="list-create-building-type",
    ),
    path(
        "building-types/<int:pk>/",
        prop_views.BuildingTypeRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-building-type",
    ),
    # ======================================================================
    # LAND TYPE ROUTES
    # ======================================================================
    path(
        "land-types/",
        prop_views.LandTypeListCreateView.as_view(),
        name="list-create-land-type",
    ),
    path(
        "land-types/<int:pk>/",
        prop_views.LandTypeRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-land-type",
    ),
    # ======================================================================
    # PROPERTY KEY FEATURES ROUTES
    # ======================================================================
    path(
        "<int:pk>/keyfeatures/",
        prop_views.PropertyKeyFeatureListCreateView.as_view(),
        name="list-create-property-key-feature",
    ),
    path(
        "keyfeatures/<int:pk>/",
        prop_views.PropertyKeyFeatureRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-key-feature",
    ),
    # ======================================================================
    # PROPERTY IMAGE LABEL ROUTES
    # ======================================================================
    path(
        "property-image-labels/",
        prop_views.PropertyImageLabelListCreateView.as_view(),
        name="list-create-property-image-label",
    ),
    path(
        "property-image-labels/<int:pk>/",
        prop_views.PropertyImageLabelRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-image-label",
    ),
    # ======================================================================
    # PROPERTY IMAGE ROUTES
    # ======================================================================
    path(
        "<int:pk>/images/",
        prop_views.PropertyImageListCreateView.as_view(),
        name="list-create-property-image",
    ),
    path(
        "propertyimages/<int:pk>/",
        prop_views.PropertyImageRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-image",
    ),
    # ======================================================================
    # PROPERTY IMAGE ROUTES
    # ======================================================================
    path(
        "<int:pk>/videos/",
        prop_views.PropertyVideoListCreateView.as_view(),
        name="list-create-property-video",
    ),
    path(
        "propertyvideos/<int:pk>/",
        prop_views.PropertyVideoRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-video",
    ),
    # ======================================================================
    # PROPERTY PLAN ROUTES
    # ======================================================================
    path(
        "<int:pk>/plans/",
        prop_views.PropertyPlanListCreateView.as_view(),
        name="list-create-property-plan",
    ),
    path(
        "plans/<int:pk>/",
        prop_views.PropertyPlanRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-property-plan",
    ),
    # ======================================================================
    # PROPERTY ROUTES
    # ======================================================================
    path("create/", prop_views.PropertyCreateView.as_view(), name="create-property"),
    path(
        "agent/<int:pk>/",
        prop_views.AgentPropertyRetrieveUpdateDestroyView.as_view(),
        name="agent-retrieve-update-destroy-property",
    ),
    path(
        "agent/list/",
        prop_views.PropertyListByAgentView.as_view(),
        name="agent-list-property",
    ),
    path(
        "admin/<int:pk>/",
        prop_views.AdminPropertyRetrieveUpdateDestroyView.as_view(),
        name="admin-retrieve-update-destroy-property",
    ),
    path(
        "admin/list/",
        prop_views.PropertyListByAdminView.as_view(),
        name="admin-list-property",
    ),
    # path(
    #     "list-property-by-agent-branch/<int:agent_branch>/",
    #     prop_views.PropertyListByAgentBranchView.as_view(),
    #     name="list-property-by-agent-branch",
    # ),
    # ======================================================================
    # APARTMENT ROUTES
    # ======================================================================
    path(
        "apartments/<int:pk>/",
        prop_views.ApartmentRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-apartment",
    ),
    path(
        "apartments/<int:apartment_id>/units/",
        prop_views.ApartmentUnitListCreateByApartmentView.as_view(),
        name="list-apartment-units-by-apartment",
    ),
    path(
        "apartments-by-agent/<int:agent_id>/",
        prop_views.ApartmentListByAgentView.as_view(),
        name="list-apartment-by-agent",
    ),
    path(
        "apartments/units/<int:pk>/",
        prop_views.ApartmentUnitRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-apartment-unit",
    ),
    # ======================================================================
    # SHAREHOUSE ROUTES
    # ======================================================================
    path(
        "sharehouses/<int:pk>/",
        prop_views.SharehouseRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-sharehouse",
    ),
    path(
        "sharehouses/<int:sharehouse_id>/rooms/",
        prop_views.RoomListCreateBySharehouseView.as_view(),
        name="list-create-rooms-by-sharehouse",
    ),
    path(
        "sharehouses-by-agent/<int:agent_id>/",
        prop_views.SharehouseListByAgentView.as_view(),
        name="list-sharehouse-by-agent",
    ),
    path(
        "sharehouses/rooms/<int:pk>/",
        prop_views.SharehouseRoomRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-sharehouse-unit",
    ),
    # ======================================================================
    # VILLA ROUTES
    # ======================================================================
    path(
        "villas/<int:pk>/",
        prop_views.VillaRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-villa",
    ),
    path(
        "villas-by-agent/<int:agent_id>/",
        prop_views.VillaListByAgentView.as_view(),
        name="list-villas-by-agent",
    ),
    # ======================================================================
    # CONDOMINIUM ROUTES
    # ======================================================================
    path(
        "condominiums/<int:pk>/",
        prop_views.CondominiumRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-condominium",
    ),
    path(
        "condominiums-by-agent/<int:agent_id>/",
        prop_views.CondominiumListByAgentView.as_view(),
        name="list-condominiums-by-agent",
    ),
    # ======================================================================
    # TOWNHOUSE ROUTES
    # ======================================================================
    path(
        "townhouses/<int:pk>/",
        prop_views.TownhouseRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-townhouse",
    ),
    path(
        "townhouses-by-agent/<int:agent_id>/",
        prop_views.TownhouseListByAgentView.as_view(),
        name="list-townhouses-by-agent",
    ),
    # ======================================================================
    # VENUE ROUTES
    # ======================================================================
    path(
        "venues/<int:pk>/",
        prop_views.VenueRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-venue",
    ),
    path(
        "venues-by-agent/<int:agent_id>/",
        prop_views.VenueListByAgentView.as_view(),
        name="list-venues-by-agent",
    ),
    # ======================================================================
    # LAND ROUTES
    # ======================================================================
    path(
        "lands/<int:pk>/",
        prop_views.LandRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-land",
    ),
    path(
        "lands-by-agent/<int:agent_id>/",
        prop_views.LandListByAgentView.as_view(),
        name="list-lands-by-agent",
    ),
    # ======================================================================
    # COMMERCIAL PROPERTY ROUTES
    # ======================================================================
    path(
        "commercialproperties/<int:pk>/",
        prop_views.CommercialPropertyRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-commercialproperty",
    ),
    path(
        "commercialproperties-by-agent/<int:agent_id>/",
        prop_views.CommercialPropertyListByAgentView.as_view(),
        name="list-commercialproperties-by-agent",
    ),
    path(
        "offices-by-agent/<int:agent_id>/",
        prop_views.OfficeListByAgentView.as_view(),
        name="list-offices-by-agent",
    ),
    path(
        "othercommercialpropertyunits-by-agent/<int:agent_id>/",
        prop_views.OtherComemrcialPropertyUnitListByAgentView.as_view(),
        name="list-offices-by-agent",
    ),
    path(
        "commercialproperties/<int:commercialproperty_id>/offices/",
        prop_views.OfficeListCreateByCommercialPropertyView.as_view(),
        name="list-create-offices-by-commercialproperty",
    ),
    path(
        "commercialproperties/offices/<int:pk>/",
        prop_views.OfficeRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-office",
    ),
    path(
        "commercialproperties/<int:commercialproperty_id>/otherunits/",
        prop_views.OtherUnitListCreateByCommercialPropertyView.as_view(),
        name="list-create-otherunit-by-commercialproperty",
    ),
    path(
        "commercialproperties/otherunits/<int:pk>/",
        prop_views.OtherCommercialPropertyUnitRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy-otherunit",
    ),
    # ======================================================================
    # PROPERTY CATEGORY AMENITY
    # ======================================================================
    path(
        "categories/<int:property_category_id>/amenities/",
        prop_views.PropertyCategoryAmenityCreateListView.as_view(),
        name="list-create-property-category-amenity",
    ),
    path(
        "categories/<int:property_category_id>/amenities/<int:property_category_amenity_id>/",
        prop_views.PropertyCategoryAmenityRetrieveDestroyView.as_view(),
        name="retrieve-delete-property-category-amenity",
    ),
    # ======================================================================
    # PROPERTY AMENITY
    # ======================================================================
    path(
        "<int:property_id>/amenities/",
        prop_views.PropertyAmenityCreateListView.as_view(),
        name="list-create-property-amenity",
    ),
    # ======================================================================
    # APARTMENT UNIT AMENITY
    # ======================================================================
    path(
        "apartmentunits/<int:apartmentunit_id>/amenities/",
        prop_views.ApartmentUnitAmenityCreateListView.as_view(),
        name="list-create-apartment-unit-amenity",
    ),
    # ======================================================================
    # OFFICE UNIT AMENITY
    # ======================================================================
    path(
        "officeunits/<int:officeunit_id>/amenities/",
        prop_views.OfficeUnitAmenityCreateListView.as_view(),
        name="list-create-office-unit-amenity",
    ),
    # ======================================================================
    # OTHER COMMERCIAL PROPERTY UNIT AMENITY
    # ======================================================================
    path(
        "othercommercialpropertyunits/<int:othercommercialpropertyunits_id>/amenities/",
        prop_views.OtherCommercialPropertyUnitAmenityCreateListView.as_view(),
        name="list-create-office-unit-amenity",
    ),
]
