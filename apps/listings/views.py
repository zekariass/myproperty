from datetime import timedelta
from django.forms import model_to_dict
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from apps.agents.views import update_agent_discount_tracker
from apps.listings.tasks import send_new_listing_added_email_to_agent
from apps.mixins.custom_pagination import GeneralCustomPagination

from apps.properties import models as prop_models
from apps.agents import models as agent_models

from apps.mixins.permissions import (
    IsAdminUserOrReadOnly,
    IsAgent,
    IsAgentOrReadOnly,
    ReadOnly,
)
from apps.mixins import constants
from apps.mixins.functions import get_boolean_url_query_value
from apps.mixins.functions import get_success_response_dict, get_error_response_dict
from apps.system import models as sys_models
from django.db import connection, transaction

from . import models as listing_models
from . import serializers as listing_serializers


class ListingCreateView(CreateAPIView):
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
                    get_error_response_dict(
                        message=f"Property with id {_property} is not found!"
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                # RETRIEVE AGENT BRANCH FROM DB
                agent_branch_instance = agent_models.AgentBranch.objects.get(
                    id=_agent_branch
                )
            except ObjectDoesNotExist:
                return Response(
                    get_error_response_dict(
                        message=f"Agent branch with id {_agent_branch} is not found!"
                    ),
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
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
                _sub_listing_serializer = (
                    listing_serializers.SharehouseListingSerializer
                )
                # _unit_name = "room"

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
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            update_agent_discount_tracker(agent_branch_instance.agent.id)

            send_new_listing_added_email_to_agent(
                agent_branch=agent_branch_instance.id,
                property_category_name=_property_category.name,
                property_address=model_to_dict(property_instance.address),
                listing_id=listing_instance.id,
            )

            return Response(
                get_success_response_dict(data=listing_serializer.data),
                status=status.HTTP_201_CREATED,
            )

    # @method_decorator(cache_page(60 * 60 * 2))
    # @method_decorator(
    #     vary_on_headers(
    #         "Authorization",
    #     )
    # )
    # def get(self, request):
    #     return get_constructed_lookup_and_order_by_params(self, request)

    # def get_queryset(self):
    # GET LISTINGS FOR SPECIFIC AGENT
    # queryset = super().get_queryset()
    # print("QQQ=====================QQQ=>: ", len(connection.queries))

    # return queryset
    # if "agent" not in self.request.query_params:
    #     return []

    # return get_constructed_lookup_and_order_by_params(self)


class ListingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
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
                    get_error_response_dict(message=f"Listing with id {pk} not found!"),
                    status=status.HTTP_404_NOT_FOUND,
                )

            # CHECK IF LISTING TYPE IS CHANGED. LISTING TYPE CAN NOT BE CHANGED, SUCH AS FROM RENT TO SALE
            if (
                "listing_type" in request.data
                and listing_instance.listing_type != request.data["listing_type"]
            ):
                return Response(
                    get_error_response_dict(
                        message=f"Listing type can not be changed from {listing_instance.listing_type} to {request.data['listing_type']}"
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF LISTING TYPE IS CHANGED. LISTING TYPE CAN NOT BE CHANGED, SUCH AS FROM RENT TO SALE
            if (
                "listing_payment_type" in request.data
                and listing_instance.listing_payment_type
                != request.data["listing_payment_type"]
            ):
                return Response(
                    get_error_response_dict(
                        message=f"Listing payment type can not be changed from {listing_instance.listing_payment_type} to {request.data['listing_payment_type']}"
                    ),
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
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF THE LISTING TYPE AND RETRIEVE LISTING TYPE DATA INSTANCE AND GET SERIALIZER
            if listing_instance.listing_type == constants.LISTING_TYPE_RENT:
                try:
                    # RETRIEVE RENT LISTING INSTANCE
                    listing_type_data_instance = listing_models.RentListing.objects.get(
                        id=listing_type_data["id"]
                    )
                except:
                    return Response(
                        get_error_response_dict(
                            message=f"Rent listing with id {listing_type_data['id']} not found!"
                        ),
                        status=status.HTTP_404_NOT_FOUND,
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
                        get_error_response_dict(
                            message=f"Sale listing with id {listing_type_data['id']} not found!"
                        ),
                        status=status.HTTP_404_NOT_FOUND,
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
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                get_success_response_dict(
                    data={
                        "listing": listing_serializer.data,
                        "listing_type_data": listing_type_serilaizer.data,
                    }
                ),
                status=status.HTTP_200_OK,
            )


class PublicListingListUsingQuryParamAPIView(ListAPIView):
    """List all listings. For Public use"""

    queryset = listing_models.Listing.objects.all()
    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [ReadOnly]
    pagination_class = GeneralCustomPagination

    def get(self, request):
        try:
            # CHECK IF AGENT IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
            # IT ALLOWS TO LIST LISTINGS FROM A SPECIFIC AGENT
            agent = None
            if "agent" in request.query_params:
                agent = request.query_params["agent"]

            # CHECK IF AGENT BRANCH IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
            # IT ALLOWS TO LIST LISTINGS FROM A SPECIFIC AGENT BRANCH
            agent_branch = None
            if "agent_branch" in request.query_params:
                agent_branch = request.query_params["agent_branch"]

            # CONSTRUCT QUERY LOOKUP PARAMS AND ORDERING PARAM FROM THE INCOMING QUERY PARAMS
            constructed_lookups, order_by = get_constructed_lookup_and_order_by_params(
                self,
                request,
                own_agent=None,
                agent_query=agent,
                own_agent_branch=None,
                agent_branch_query=agent_branch,
            )

            # FILTER LISTING USING THE CONSTRUCTED LOOKUP PARAMS AND ORDER BY THE ORDERING PARAM
            result_listings = (
                listing_models.Listing.objects.select_related(
                    "main_property",
                    "main_property__property_category",
                    "main_property__address",
                )
                .filter(*constructed_lookups)
                .distinct()
                .order_by(order_by)
            )

            # PAGINATE THE RESPONSE
            paginator = self.pagination_class()
            paginated_listings = paginator.paginate_queryset(result_listings, request)
            listing_serializer = self.get_serializer(
                instance=paginated_listings, many=True
            )

            return paginator.get_paginated_response(listing_serializer.data)
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class AgentListingListUsingQuryParamAPIView(ListAPIView):
    """List all listings. For Agent use only"""

    queryset = listing_models.Listing.objects.all()
    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [IsAgent]
    pagination_class = GeneralCustomPagination

    def get(self, request):
        try:
            user = request.user

            # CHECK IF AGENT BRANCH IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
            # IT ALLOWS TO LIST LISTINGS FROM A SPECIFIC AGENT BRANCH
            _agent_branch_query = None
            if "agent_branch" in request.query_params:
                _agent_branch_query = request.query_params.pop("agent_branch")

            # GET THE AGENT ADMIN ASSOCIATED WITH CURRENT USER
            # IF NO AGENT ADMIN OBJECT FOUND, REPLY ERROR
            agent_admin_instance = agent_models.AgentAdmin.objects.select_related(
                "agent_branch", "agent_branch__agent"
            ).filter(user=user.id)

            if not agent_admin_instance.exists():
                return Response(
                    get_error_response_dict(
                        message="You need to signin as Agent to access your listings"
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # GET THE AGENT AND AGENT BRANCH THE CURRENT USER IS WORKING IN
            own_agent_branch = agent_admin_instance.first().agent_branch
            own_agent = own_agent_branch.agent

            # VARIABLE WHICH HOLDS THE AGENT BRANCH ID FROM QUERY PARAM
            agent_branch_query = None

            # IF THE AGENT BRANCH THAT THE CURRENT USER IS WORKING IS A MAIN BRANCH,
            # THE USER CAN ACCESS OTHER AGENT BRANCHES LISTING OF THE SAME AGENT
            # GET THE AGENT BRANCH USING THE AGENT BRANCH ID FROM QUERY PARAM AND COMPARE
            # WITH USERS OWN AGENT. IF EQUAL, THEN ADD THE AGENT BRANCH QUERY PARAM IN THE LOOKUP
            if (
                agent_admin_instance.first().agent_branch.is_main_branch
                and _agent_branch_query
            ):
                query_agent_branch_instance = agent_models.AgentBranch.objects.filter(
                    id=_agent_branch_query
                ).first()
                if (
                    query_agent_branch_instance
                    and query_agent_branch_instance.agent == own_agent
                ):
                    agent_branch_query = _agent_branch_query

            # CONTRUCT THE LOOKUP AND ORDERING PARAMS FROM QUERY PARAMS
            (
                constructed_lookups,
                order_by,
            ) = get_constructed_lookup_and_order_by_params(
                self,
                request,
                own_agent=own_agent.id,
                own_agent_branch=own_agent_branch.id,
                agent_branch_query=agent_branch_query,
            )

            # GET THE LISTINGS BASED ON THE CONSTRUCTED LOOKUP PARAMS AND ORDER BY THE ORDERING PARAMS
            result_listings = (
                listing_models.Listing.objects.select_related(
                    "main_property",
                    "main_property__property_category",
                    "main_property__address",
                )
                .filter(*constructed_lookups)
                .distinct()
                .order_by(order_by)
            )

            # PAGINATE THE RESPONSE
            paginator = self.pagination_class()
            paginated_listing = paginator.paginate_queryset(result_listings, request)

            listing_serializer = self.get_serializer(
                instance=paginated_listing, many=True
            )

            return paginator.get_paginated_response(listing_serializer.data)
        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


class AdminListingListUsingQuryParamAPIView(ListAPIView):
    """List all listings. For admin use only"""

    queryset = listing_models.Listing.objects.all()
    serializer_class = listing_serializers.ListingSerializer
    permission_classes = [IsAdminUser]
    pagination_class = GeneralCustomPagination

    def get(self, request):
        try:
            # CHECK IF AGENT IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
            # IT ALLOWS TO LIST LISTINGS FROM A SPECIFIC AGENT
            agent = None
            if "agent" in request.query_params:
                agent = request.query_params.pop("agent")

            # CHECK IF AGENT BRANCH IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
            # IT ALLOWS TO LIST LISTINGS FROM A SPECIFIC AGENT BRANCH
            agent_branch = None
            if "agent_branch" in request.query_params:
                agent_branch = request.query_params.pop("agent_branch")

            # CONTRUCT THE LOOKUP AND ORDERING PARAMS FROM QUERY PARAMS
            (
                constructed_lookups,
                order_by,
            ) = get_constructed_lookup_and_order_by_params(
                self,
                request,
                own_agent=None,
                agent_query=agent,
                own_agent_branch=None,
                agent_branch_query=agent_branch,
            )

            # GET THE LISTINGS BASED ON THE CONSTRUCTED LOOKUP PARAMS AND ORDER BY THE ORDERING PARAMS
            result_listings = (
                listing_models.Listing.objects.select_related(
                    "main_property",
                    "main_property__property_category",
                    "main_property__address",
                )
                .filter(*constructed_lookups)
                .distinct()
                .order_by(order_by)
            )

            # PAGINATE THE RESPONSE
            paginator = self.pagination_class()
            paginated_listings = paginator.paginate_queryset(result_listings, request)
            listing_serializer = self.get_serializer(
                instance=paginated_listings, many=True
            )

            return paginator.get_paginated_response(listing_serializer.data)

        except Exception as e:
            return Response(
                get_error_response_dict(message=str(e)),
                status=status.HTTP_400_BAD_REQUEST,
            )


def get_constructed_lookup_and_order_by_params(
    self,
    request,
    own_agent=None,
    agent_query=None,
    own_agent_branch=None,
    agent_branch_query=None,
):
    """
    Construct lookup and ordering params from the url query parameters.
    The client can flexibly set query params, like:

    ?is_active=true&agent=1&is_approved=false&is_featured=false&is_featuring_approved=false.

    It is possible to set all or anyone or none of the following parameters.

    ######################################
    Search params:
        ** For all property types:
            - min_price
            - max_price
            - property_category => send property_category_key
            - location
            - location_radius
            - added_since => ie. 10_days, 24_hours, 1_week, 3_weeks, etc
        ** For all residential properties
            - min_beds
            - max_beds
        ** For sharehouse
            - min_rooms
            - max_rooms
        ** For Commercial Property
            - commercial_type
        ** For Land Poperty
            - min_land_area
            - max_land_area
            - land_type
        ** Other search params
            - agent
            - agent_branch
            - listing_type
            - is_active
            - is_expired
            - is_approved
            - is_featured
            - is_featuring_approved
    Sorting Params:
        - sort_by
    """

    agent = agent_query if agent_query else own_agent

    agent_branch = agent_branch_query if agent_branch_query else own_agent_branch

    listing_type = (
        request.query_params["listing_type"].upper()
        if "listing_type" in request.query_params
        else None
    )

    # IF LISTING TYPE IS ANY, DO NOT SET LISTING TYPE OR SET TO NONE INSTEAD
    if listing_type and listing_type.upper() == "ANY":
        listing_type = None

    # get_boolean_url_query_value is a function which returns a parsed boolean query param value
    is_active = get_boolean_url_query_value(request, "is_active")
    is_expired = get_boolean_url_query_value(request, "is_expired")
    is_approved = get_boolean_url_query_value(request, "is_approved")
    is_featured = get_boolean_url_query_value(request, "is_featured")
    is_featuring_approved = get_boolean_url_query_value(
        request, "is_featuring_approved"
    )

    # DICT OBJECT WHICH HOLDS GENERAL LOOKUP PARAMS
    general_lookups = {}

    # LIST WHICH WILL HOLD ALL LOOKUP PARAMS
    all_lookup_params = []
    if agent:
        general_lookups["agent_branch__agent"] = agent
    if agent_branch:
        general_lookups["agent_branch"] = agent_branch
    if listing_type:
        general_lookups["listing_type"] = listing_type
    if is_active is not None:
        general_lookups["is_active"] = is_active
    if is_expired is not None:
        general_lookups["is_expired"] = is_expired
    if is_featured is not None:
        general_lookups["is_featured"] = is_featured

    # Check if is_approved query param is None. If None that means it is not sent as query param
    if is_approved is not None:
        # Check if is_approved is sent as false or true in the query param
        if is_approved:
            is_approved_q_lookup = Q(listing_payment__is_approved=is_approved)
        else:
            is_approved_q_lookup = Q(Q(listing_payment=None) | Q(listing_payment=False))

        # Append the Q query lookup object to the list
        all_lookup_params.append(is_approved_q_lookup)

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
        all_lookup_params.append(is_featuring_approved_q_lookup)

    general_q_lookup = Q(**general_lookups)

    # ========PROPERTY RELATED LOOKUPS===================
    property_related_common_lookups = {}

    # PROPERTY PRICE LOOKUP
    min_price = (
        request.query_params["min_price"]
        if "min_price" in request.query_params
        else None
    )
    max_price = (
        request.query_params["max_price"]
        if "max_price" in request.query_params
        else None
    )

    # ADDED TO SITE DATE LOOKUP
    added_since = (
        request.query_params["added_since"]
        if "added_since" in request.query_params
        else None
    )

    # PROPERTY CATEGORY LOOKUP
    property_category = (
        request.query_params["property_category"]
        if "property_category" in request.query_params
        else None
    )

    # IF BOTH MIN PRICE AND MAX PRICE ARE PROVIDED
    if min_price and max_price:
        property_related_common_lookups["property_price__range"] = (
            min_price,
            max_price,
        )
    # IF ONLY MIN PRICE PROVIDED
    elif min_price:
        property_related_common_lookups["property_price__gte"] = min_price

    # IF ONLY MAX PRICE PROVIDED
    elif max_price:
        property_related_common_lookups["property_price__lte"] = max_price

    # IF ADDED DATE QUERY PARAM PROVIDED
    if added_since:
        if "hour" in added_since:
            time_delta = timezone.timedelta(hours=int(added_since.split("_")[0]))
        elif "day" in added_since:
            time_delta = timezone.timedelta(days=int(added_since.split("_")[0]))
        elif "week" in added_since:
            time_delta = timezone.timedelta(weeks=int(added_since.split("_")[0]))
        property_related_common_lookups["added_on__gte"] = timezone.now() - time_delta

    # IF PROPERTY CATEGORY IS PROVIDED IN QUERY PARAM
    if property_category:
        property_related_common_lookups[
            "main_property__property_category__cat_key"
        ] = property_category

    common_q_lookup = Q(**property_related_common_lookups)

    # ========RESIDENTIAL PROPERTY LOOKUP ==============================================
    residential_property_q_lookup = Q()

    # MINIMUM NUMBER OF BEDS LOOKUP PARAM
    min_beds = (
        request.query_params["min_beds"] if "min_beds" in request.query_params else None
    )

    # MAXIMUM NUMBER OF BEDS LOOKUP PARAM
    max_beds = (
        request.query_params["max_beds"] if "max_beds" in request.query_params else None
    )

    # IF BOTH MIN BEDS AND MAX BEDS ARE PROVIDED
    # IF PROPERTY CATEGORY IS PROVIDED IN THE QUERY PARAMS,
    # FILTER NUMBER OF BEDS BASED ON THE PROPERTY CATEGORY
    if (min_beds or max_beds) and property_category:
        if property_category == constants.APARTMENT_KEY:
            residential_property_q_lookup = Q(
                apartmentunitlisting__apartment_unit__bed_rooms__range=(
                    min_beds,
                    max_beds,
                )
            )
        elif property_category == constants.CONDOMINIUM_KEY:
            residential_property_q_lookup = Q(
                condominiumlisting__condominium__bed_rooms__range=(min_beds, max_beds)
            )
        elif property_category == constants.VILLA_KEY:
            residential_property_q_lookup = Q(
                villalisting__villa__bed_rooms__range=(min_beds, max_beds)
            )
        elif property_category == constants.TOWNHOUSE_KEY:
            residential_property_q_lookup = Q(
                townhouselisting__townhouse__bed_rooms__range=(min_beds, max_beds)
            )

    # IF PROPERTY CATEGORY IS NOT PROVIDED IN THE QUERY PARAMS
    # FILTER FROM ALL RESIDENTIAL PROPERTIES
    elif (min_beds or max_beds) and not property_category:
        residential_property_q_lookup = Q(
            Q(
                apartmentunitlisting__apartment_unit__bed_rooms__range=(
                    min_beds,
                    max_beds,
                )
            )
            | Q(condominiumlisting__condominium__bed_rooms__range=(min_beds, max_beds))
            | Q(villalisting__villa__bed_rooms__range=(min_beds, max_beds))
            | Q(townhouselisting__townhouse__bed_rooms__range=(min_beds, max_beds))
        )

    # ===================SHARE HOUSE LOOKUP ===================================
    # IF MINIMUM NUMBER OF ROOMS PROVIDED IN THE QUERY PARAM
    min_rooms = (
        request.query_params["min_rooms"]
        if "min_rooms" in request.query_params
        else None
    )
    # IF MAXIMUM NUMBER OF ROOMS PROVIDED IN THE QUERY PARAM
    max_rooms = (
        request.query_params["max_rooms"]
        if "max_rooms" in request.query_params
        else None
    )

    sharehouse_property_q_lookup = Q()

    # IF BOTH MINIMUM AND MAXIMUM NUMBER OF ROOMS PROVIDED IN THE QUERY PARAM AND
    # PROPERTY CATEGORY IS NOT PROVIDED, RAISE EXCEPTION
    if (min_rooms or max_rooms) and not property_category:
        raise Exception(
            f"Please select house shareproperty category to get properties with {min_rooms or max_rooms} rooms."
        )

    # IF BOTH MINIMUM AND MAXIMUM NUMBER OF ROOMS PROVIDED IN THE QUERY PARAM AND
    # PROPERTY CATEGORY IS  PROVIDED, FILTER FROM ROOMS TABLE
    if (min_rooms or max_rooms) and property_category == constants.SHAREHOUSE_KEY:
        if not min_rooms:
            min_rooms = 0
        if not max_rooms:
            max_rooms = 999
        sharehouse_property_q_lookup = Q(
            main_property__sharehouse__room__bed_rooms__range=(min_rooms, max_rooms)
        )

    # =================== GET COMMERCIAL PROPERTY LOOKUP =====================
    # ** For Commercial Property
    #         - commercial_type

    commercial_property_q_lookup = Q()

    # IF COMMERCIAL TYPE IS PROVIDED IN QUERY PARAMS
    if "commercial_type" in request.query_params:
        if "OFFICE" in request.query_params["commercial_type"].upper():
            # CHECK IF officelisting ATTRIBUTE OF LISTING IS NULL
            commercial_property_q_lookup = Q(officelisting__isnull=False)
        elif "OTHER" in request.query_params["commercial_type"].upper():
            # CHECK IF othercommercialpropertyunitlisting ATTRIBUTE OF LISTING IS NULL
            commercial_property_q_lookup = Q(
                othercommercialpropertyunitlisting__isnull=False
            )

    # =================== GET LAND PROPERTY LOOKUP =====================
    #     ** For Land Poperty
    #         - min_land_area
    #         - max_land_area
    #         - land_type

    # IF min_land_area IS PROVIDED IN THE QUERY PARAMS
    min_land_area = (
        request.query_params["min_land_area"]
        if "min_land_area" in request.query_params
        else None
    )

    # IF max_land_area IS PROVIDED IN THE QUERY PARAMS
    max_land_area = (
        request.query_params["max_land_area"]
        if "max_land_area" in request.query_params
        else None
    )

    # IF max_land_area IS PROVIDED IN THE QUERY PARAMS
    land_type = (
        request.query_params["land_type"]
        if "land_type" in request.query_params
        else None
    )

    # IF BOTH min_land_area  AND max_land_area PROVIDED IN THE QUERY PARAMS, BUT
    # property_category NOT PROVIDED, OR
    # IF land_type IS PROVIDED IN THE QUERY PARAMS AND
    # property_category NOT PROVIDED, OR
    # RAISE EXCEPTION
    if (
        (min_land_area or max_land_area)
        and not property_category
        or (land_type and not property_category)
    ):
        raise Exception(
            f"Please select Land property category to get lands with {min_land_area or max_land_area} area."
        )
    land_property_q_lookup = Q()

    # OTHERWISE FILTER LAND LISTINGS WITH SPECIFIED OR DEFAULT LAND AREA
    if (min_land_area or max_land_area) and property_category == constants.LAND_KEY:
        if not min_land_area:
            min_land_area = 0
        if not max_land_area:
            max_land_area = 999999999
        land_property_q_lookup = Q(
            main_property__land__area__range=(min_land_area, max_land_area)
        )

    # IF LAND TYPE IS PROVIDED IN THE QUERY PARAMS, ADD IT TO THE LOOKUP
    if land_type:
        land_property_q_lookup = Q(
            land_property_q_lookup
            & Q(main_property__land__land_type__name__icontains=land_type)
        )

    # ======== LOCATION LOOKUP ================================================
    # LOCATION RADIUS FILTER TO LOOKUP PROPERTIES WITHIN RANGE OF LOCATION AREA
    # TODO
    # location_radius = (
    #     request.query_params["location_radius"]
    #     if request.query_params["location_radius"]
    #     else None
    # )

    location_q_lookup = Q()

    # IF LOCATION IS PROVIDED IN THE QUERY PARAMS
    location = (
        request.query_params["location"] if "location" in request.query_params else None
    )

    # IF LOCATION IS NOT NONE
    if location:
        location_q_lookup = Q(
            Q(main_property__address__city__icontains=location)
            | Q(main_property__address__street__icontains=location)
            | Q(main_property__address__post_code__icontains=location)
        )

    # ====================Append the Q query lookup objects to the list ============
    all_lookup_params.append(general_q_lookup)
    all_lookup_params.append(common_q_lookup)
    all_lookup_params.append(residential_property_q_lookup)
    all_lookup_params.append(sharehouse_property_q_lookup)
    all_lookup_params.append(location_q_lookup)
    all_lookup_params.append(commercial_property_q_lookup)
    all_lookup_params.append(land_property_q_lookup)

    # ======= CONSTRUCT ORDERING PARAM FROM QUERY PARAM OR SET ITS DEFAULT ===========
    order_by = "added_on"

    # IF SORT BY IS PROVIDED IN THE QUERY PARAMS
    if "sort_by" in request.query_params:
        order_by = request.query_params["sort_by"]

    # print("======================>: ", len(connection.queries))
    return (all_lookup_params, order_by)
