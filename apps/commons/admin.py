from django.contrib import admin

from . import models as cmns_model

admin.site.register(cmns_model.Country)
admin.site.register(cmns_model.Address)