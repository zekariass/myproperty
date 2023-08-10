from datetime import timedelta
from django.forms import model_to_dict
from django.shortcuts import render
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from apps.agents.views import update_agent_discount_tracker
from apps.commons.models import Tag
from apps.listings.tasks import send_new_listing_added_email_to_agent

from apps.properties import models as prop_models
from apps.agents import models as agent_models

from apps.mixins.permissions import IsAdminUserOrReadOnly, IsAgentOrReadOnly
from apps.mixins import constants
from apps.mixins.functions import get_boolean_url_query_value
from apps.system import models as sys_models
from django.db import transaction

from . import models as listing_models
from . import serializers as listing_serializers


def get_listings_list_using_url_query_param(self):
    """
    Listing listings based on the url query parameter from the client application.
    The client can flexibly set query params, like:

    ?is_active=true&agent=1&is_approved=false&is_featured=false&is_featuring_approved=false.

    It is possible to set all or anyone or none of the following parameters.
    """
    agent = (
        int(self.request.query_params["agent"])
        if "agent" in self.request.query_params
        else None
    )
    agent_branch = (
        int(self.request.query_params["agent_branch"])
        if "agent_branch" in self.request.query_params
        else None
    )

    # get_boolean_url_query_value is a function which returns a parsed boolean query param value
    is_active = get_boolean_url_query_value(self.request, "is_active")
    is_expired = get_boolean_url_query_value(self.request, "is_expired")
    is_approved = get_boolean_url_query_value(self.request, "is_approved")
    is_featured = get_boolean_url_query_value(self.request, "is_featured")
    is_featuring_approved = get_boolean_url_query_value(
        self.request, "is_featuring_approved"
    )

    # Dict object to hold some of query lookups based on query parameter
    lookups = {}

    # List to hold all the Q query objects
    all_lookups = []
    if agent:
        lookups["agent_branch__agent"] = agent
    if agent_branch:
        lookups["agent_branch"] = agent_branch
    if is_active is not None:
        lookups["is_active"] = is_active
    if is_expired is not None:
        lookups["is_expired"] = is_expired
    if is_featured is not None:
        lookups["is_featured"] = is_featured
    # Check if is_approved query param is None. If None that means it is not sent as query param
    if is_approved is not None:
        # Check if is_approved is sent as false or true in the query param
        if is_approved:
            is_approved_q_lookup = Q(listing_payment__is_approved=is_approved)
        else:
            is_approved_q_lookup = Q(Q(listing_payment=None) | Q(listing_payment=False))

        # Append the Q query lookup object to the list
        all_lookups.append(is_approved_q_lookup)

    # Check if is_featuring_approved is None. If None that means it is not sent as query param
    # is_featuring_approved is approval status of featuring, which is to be obtained from featuring_payment field
    if is_featuring_approved is not None:
        # Check if is_featuring_approved is sent as false or true in the query param
        if is_featuring_approved:
            is_featuring_approved_q_lookup = Q(
                featuring_payment__is_approved=is_featuring_approved
            )
        else:
            is_featuring_approved_q_lookup = Q(
                Q(featuring_payment=None) | Q(featuring_payment=False)
            )
        # Append the Q query lookup object to the list
        all_lookups.append(is_featuring_approved_q_lookup)

    rest_q_lookup = Q(**lookups)

    # Append the Q query lookup object to the list
    all_lookups.append(rest_q_lookup)

    # Filter Listing by the constructed Q lookup object
    result_listings = listing_models.Listing.objects.filter(*all_lookups)
    return result_listings


class ListingListCreateView(ListCreateAPIView):
    queryset = listing_models.Listing.objects.all()
    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAgentOrReadOnly]

    def post(self, request):
        # print(request.data)

        # POP LISTING TYPE DATA, WHICH MUST BE EITHER RENT OR SALE
        listing_type_data = request.data.pop("listing_type_data")

        # POP SUBLISTING DATA, SUCH AS APARTMENT LISTING, CONDOMINIUM LISTING, ETC
        sub_listing_data = request.data.pop("sub_listing_data")

        # ALL DATABASE OPERATIONS FOR LISTING MUST TAKE PLACE IN ATOMIC
        with transaction.atomic():
            # GET PROPERTY ID FROM INCOMMING DATA
            _property = request.data["main_property"]

            # GET AGENT BRANCH ID FROM INCOMMING DATA
            _agent_branch = request.data["agent_branch"]
            try:
                # RETRIEVE PROPERTY FROM DB
                property_instance = prop_models.Property.objects.get(id=_property)
            except ObjectDoesNotExist:
                return Response(
                    {"error": f"Property with id {_property} is not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                # RETRIEVE AGENT BRANCH FROM DB
                agent_branch_instance = agent_models.AgentBranch.objects.get(
                    id=_agent_branch
                )
            except ObjectDoesNotExist:
                return Response(
                    {"error": f"Property with id {_property} is not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # GET PROPERTY CATEGORY FROM THE PROPERTY
            _property_category = property_instance.property_category

            # GET AGENT FROM AGENT BRANCH
            _agent = agent_branch_instance.agent

            # # CHECK AGENTS ACTIVE SERVICE SUBSCRIPTION
            # agent_active_subscription = (
            #     agent_models.AgentServiceSubscription.objects.filter(
            #         agent=_agent.id, expire_on__gt=timezone.now()
            #     ).first()
            # )

            is_listed_by_subscription = False
            listing_payment_type = request.data.pop("listing_payment_type")

            # CHECK IF THE AGENT HAS ACTIVE SUBSCRIPTION
            if _agent.has_active_subscription:
                is_listed_by_subscription = True
                listing_payment_type = constants.LISTING_PAYMENT_TYPE_SUBSCRIPTION

            # GET LISTING EXPIRATION LIFE TIME FROM LISTING PARAMETERs
            listing_life_time = sys_models.ListingParameter.objects.get(
                name=constants.LISTING_PARAM_LISTING_LIFE_TIME
            )

            listing_expire_on = timezone.now() + timedelta(
                days=int(listing_life_time.value)
            )

            # SAVE LISTING
            listing_serializer = self.get_serializer(data=request.data)

            listing_serializer.is_valid(raise_exception=True)
            try:
                listing_instance = listing_serializer.save(
                    is_listed_by_subscription=is_listed_by_subscription,
                    agent_branch=agent_branch_instance,
                    main_property=property_instance,
                    expire_on=listing_expire_on,
                    listing_payment_type=listing_payment_type,
                )
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # CHECK IF LISTING IS OF TYPE RENT AND SAVE IF SO
            if listing_instance.listing_type == constants.LISTING_TYPE_RENT:
                rent_listing_serializer = listing_serializers.RentListingSerializer(
                    data=listing_type_data
                )
                rent_listing_serializer.is_valid(raise_exception=True)

                rent_listing_serializer.save(listing=listing_instance)

            # CHECK IF LISTING IS OF TYPE SALE AND SAVE IF SO
            elif listing_instance.listing_type == constants.LISTING_TYPE_SALE:
                listing_models.SaleListing.objects.create(listing=listing_instance)

            _sub_listing_serializer = None
            _unit_name = None

            # CHECK SUB-LISTING TYPE, SUCH AS APARTMENT LISTING, VILLA LISTING, ETC.
            # AND GET THE CORRESPONDING SERIALIZER
            if _property_category.cat_key == constants.APARTMENT_KEY:
                _sub_listing_serializer = (
                    listing_serializers.ApartmentUnitListingSerializer
                )
                _unit_name = "apartment_unit"
            elif _property_category.cat_key == constants.CONDOMINIUM_KEY:
                _sub_listing_serializer = (
                    listing_serializers.CondominiumListingSerializer
                )
            elif _property_category.cat_key == constants.VILLA_KEY:
                _sub_listing_serializer = listing_serializers.VillaListingSerializer
            elif _property_category.cat_key == constants.SHAREHOUSE_KEY:
                _sub_listing_serializer = listing_serializers.RoomListingSerializer
                _unit_name = "room"

            elif _property_category.cat_key == constants.TOWNHOUSE_KEY:
                _sub_listing_serializer = listing_serializers.TownhouseListingSerializer
            elif _property_category.cat_key == constants.VENUE_KEY:
                _sub_listing_serializer = listing_serializers.VenueListingSerializer
            elif _property_category.cat_key == constants.LAND_KEY:
                _sub_listing_serializer = listing_serializers.LandListingSerializer
            elif _property_category.cat_key == constants.COMMERCIAL_PROPERTY_KEY:
                if (
                    sub_listing_data["unit_type"]
                    == constants.OFFICE_COMMERCIAL_PROPERTY_UNIT
                ):
                    _sub_listing_serializer = (
                        listing_serializers.OfficeListingSerializer
                    )
                    _unit_name = "office_unit"

                elif (
                    sub_listing_data["unit_type"]
                    == constants.OTHER_COMMERCIAL_PROPERTY_UNIT
                ):
                    _sub_listing_serializer = (
                        listing_serializers.OtherCommercialPropertyUnitListingSerializer
                    )
                    _unit_name = "other_commercial_property_unit"

            # SAVE SUB-LISTING DATA
            if _unit_name:
                sub_listing_data[_unit_name] = sub_listing_data["unit_id"]

            sub_listing_serializer = _sub_listing_serializer(data=sub_listing_data)
            sub_listing_serializer.is_valid(raise_exception=True)

            try:
                sub_listing_serializer.save(listing=listing_instance)
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            update_agent_discount_tracker(agent_branch_instance.agent.id)

            send_new_listing_added_email_to_agent(
                agent_branch=agent_branch_instance.id,
                property_category_name=_property_category.name,
                property_address=model_to_dict(property_instance.address),
                listing_id=listing_instance.id,
            )

            return Response(
                {"data": listing_serializer.data}, status=status.HTTP_201_CREATED
            )

    def get_queryset(self):
        # GET LISTINGS FOR SPECIFIC AGENT
        if "agent" not in self.request.query_params:
            return []

        return get_listings_list_using_url_query_param(self)


class RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = listing_models.Listing.objects.all()
    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [IsAdminUserOrReadOnly, IsAgentOrReadOnly]

    def update(self, request, pk):
        with transaction.atomic():
            # POP LISTING TYPE DATA, WHICH MUST BE EITHER RENT OR SALE
            listing_type_data = request.data.pop("listing_type_data")
            # print(listing_type_data)

            try:
                # RETRIEVE LISTING INSTANCE
                listing_instance = listing_models.Listing.objects.get(pk=pk)
            except:
                return Response(
                    {"errors": f"Listing with id {pk} not found!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF LISTING TYPE IS CHANGED. LISTING TYPE CAN NOT BE CHANGED, SUCH AS FROM RENT TO SALE
            if (
                "listing_type" in request.data
                and listing_instance.listing_type != request.data["listing_type"]
            ):
                return Response(
                    {
                        "errors": f"Listing type can not be changed from {listing_instance.listing_type} to {request.data['listing_type']}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF LISTING TYPE IS CHANGED. LISTING TYPE CAN NOT BE CHANGED, SUCH AS FROM RENT TO SALE
            if (
                "listing_payment_type" in request.data
                and listing_instance.listing_payment_type
                != request.data["listing_payment_type"]
            ):
                return Response(
                    {
                        "errors": f"Listing payment type can not be changed from {listing_instance.listing_payment_type} to {request.data['listing_payment_type']}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # DESERIALIZE LISTING DATA
            listing_serializer = self.get_serializer(
                listing_instance, data=request.data
            )
            listing_serializer.is_valid(raise_exception=True)

            try:
                # SAVE LISTING SERIALIZER
                listing_serializer.save()
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # CHECK IF THE LISTING TYPE AND RETRIEVE LISTING TYPE DATA INSTANCE AND GET SERIALIZER
            if listing_instance.listing_type == constants.LISTING_TYPE_RENT:
                try:
                    # RETRIEVE RENT LISTING INSTANCE
                    listing_type_data_instance = listing_models.RentListing.objects.get(
                        id=listing_type_data["id"]
                    )
                except:
                    return Response(
                        {
                            "errors": f"Rent listing with id {listing_type_data['id']} not found!"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                _listing_type_serilaizer = listing_serializers.RentListingSerializer
            elif listing_instance.listing_type == constants.LISTING_TYPE_SALE:
                try:
                    # RETRIEVE SALE LISTING INSTANCE
                    listing_type_data_instance = listing_models.SaleListing.objects.get(
                        id=listing_type_data["id"]
                    )
                except:
                    return Response(
                        {
                            "errors": f"Sale listing with id {listing_type_data['id']} not found!"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                _listing_type_serilaizer = listing_serializers.SaleListingSerializer

            # DESERIALIZE LISTING TYPE DATA
            listing_type_serilaizer = _listing_type_serilaizer(
                listing_type_data_instance, data=listing_type_data
            )
            listing_type_serilaizer.is_valid(raise_exception=True)
            try:
                # SAVE LISTING TYPE DATA
                listing_type_serilaizer.save()
            except Exception as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {
                    "data": {
                        "listing": listing_serializer.data,
                        "listing_type_data": listing_type_serilaizer.data,
                    }
                },
                status=status.HTTP_200_OK,
            )


class ListingListUsingQuryParamAPIView(ListAPIView):
    """List all listings. For admin use only"""

    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        return get_listings_list_using_url_query_param(self)
