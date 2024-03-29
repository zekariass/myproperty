from rest_framework.serializers import ModelSerializer

from . import models as cmns_models

# ================= COUNTRY ===================================


class CountrySerializer(ModelSerializer):
    class Meta:
        model = cmns_models.Country
        fields = "__all__"


# ================= ADDRESS ===================================


class AddressSerializer(ModelSerializer):
    class Meta:
        model = cmns_models.Address
        fields = "__all__"
        read_only_fields = ["added_on"]


# ================= TAG ===================================


class TagSerializer(ModelSerializer):
    class Meta:
        model = cmns_models.Tag
        fields = "__all__"
        read_only_fields = ["added_on"]
