from django.contrib import admin

from . import models


admin.site.register(models.PropertyCategory)
admin.site.register(models.AmenityCategory)
admin.site.register(models.Amenity)
admin.site.register(models.Property)
admin.site.register(models.PropertyAmenity)
admin.site.register(models.Apartment)
admin.site.register(models.ApartmentUnit)
admin.site.register(models.ApartmentUnitAmenity)
admin.site.register(models.Condominium)
admin.site.register(models.Villa)
admin.site.register(models.Sharehouse)
admin.site.register(models.Room)
admin.site.register(models.CommercialProperty)
admin.site.register(models.OfficeUnit)
admin.site.register(models.OtherCommercialPropertyUnit)
admin.site.register(models.LandType)
admin.site.register(models.Land)
admin.site.register(models.PropertyVideo)
admin.site.register(models.PropertyPlan)
admin.site.register(models.PropertyImageLabel)
admin.site.register(models.PropertyImage)
admin.site.register(models.ListingPriceByPropertyCategory)
admin.site.register(models.ListingPriceByPropertyCategoryHistory)
admin.site.register(models.PropertyCategoryAmenity)
admin.site.register(models.OfficeUnitAmenity)
admin.site.register(models.OtherCommercialPropertyUnitAmenity)
admin.site.register(models.BuildingType)
admin.site.register(models.PropertyKeyFeature)
admin.site.register(models.Townhouse)
admin.site.register(models.Venue)
