from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from . import models as cmns_models
from . import serializers as cmns_serializers
from apps.mixins.permissions import IsAdminUserOrReadOnly


# ================= COUNTRY ===================================
class CountryListCreateView(ListCreateAPIView):
    queryset = cmns_models.Country.objects.all()
    serializer_class = cmns_serializers.CountrySerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class CountryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = cmns_models.Country.objects.all()
    serializer_class = cmns_serializers.CountrySerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


# ================= ADDRESS ===================================
class AddressListCreateView(ListCreateAPIView):
    queryset = cmns_models.Address.objects.all()
    serializer_class = cmns_serializers.AddressSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class AddressRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = cmns_models.Address.objects.all()
    serializer_class = cmns_serializers.AddressSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


# ================= TAG ==========================================
class TagListCreateView(ListCreateAPIView):
    queryset = cmns_models.Tag.objects.all()
    serializer_class = cmns_serializers.TagSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]


class TagRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = cmns_models.Tag.objects.all()
    serializer_class = cmns_serializers.TagSerializer
    permission_classes = [
        IsAdminUserOrReadOnly,
    ]
