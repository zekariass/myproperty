from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Listing)
admin.site.register(models.RentListing)
admin.site.register(models.SaleListing)
admin.site.register(models.ApartmentUnitListing)
admin.site.register(models.CondominiumListing)
admin.site.register(models.VillaListing)
admin.site.register(models.TownhouseListing)
admin.site.register(models.VenueListing)
admin.site.register(models.LandListing)
admin.site.register(models.OfficeListing)
admin.site.register(models.OtherCommercialPropertyUnitListing)
admin.site.register(models.SavedListing)
