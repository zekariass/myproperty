from rest_framework.response import Response
from django.db import IntegrityError, connection, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.db.models import Q

from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from apps.agents.models import AgentAdmin, AgentBranch

from apps.properties import tasks

from . import models as prop_models
from . import serializers as prop_serializers

from apps.commons.serializers import AddressSerializer
from apps.mixins.permissions import (
    DoesAgentOwnThisProperty,
    IsAdminUserOrReadOnly,
    IsAuthorizedAgentAdmin,
    IsAgent,
)
from apps.mixins.functions import (
    generate_custom_property_id,
    get_boolean_url_query_value,
)
from apps.mixins import constants
from apps.mixins.custom_pagination import GeneralCustomPagination
from apps.mixins.functions import get_success_response_dict, get_error_response_dict


# ====================== AMENITY CATEGORY ====================================
class AmenityCategoryListCreateView(ListCreateAPIView):
    queryset = prop_models.AmenityCategory.objects.all()
    serializer_class = prop_serializers.AmenityCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = GeneralCustomPagination


class AmenityCategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.AmenityCategory.objects.all()
    serializer_class = prop_serializers.AmenityCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== AMENITY ==============================================
class AmenityListCreateView(ListCreateAPIView):
    queryset = prop_models.Amenity.objects.all()
    serializer_class = prop_serializers.AmenitySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class AmenityRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Amenity.objects.all()
    serializer_class = prop_serializers.AmenitySerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== PROPERTY CATEGORY ====================================
class PropertyCategoryListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


class PropertyCategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyCategory.objects.all()
    serializer_class = prop_serializers.PropertyCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== LISTING PRICE BY PROPERTY CATEGORY =====================
class ListingPriceByPropertyCategoryListCreateView(ListCreateAPIView):
    queryset = prop_models.ListingPriceByPropertyCategory.objects.all()
    serializer_class = prop_serializers.ListingPriceByPropertyCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                self.perform_create(serializer)
            except Exception as e:
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_409_CONFLICT,
                )

        return Response(get_success_response_dict(data=serializer.data), status=201)


class ListingPriceByPropertyCategoryRetrieveUpdateDestroyView(
    RetrieveUpdateDestroyAPIView
):
    queryset = prop_models.ListingPriceByPropertyCategory.objects.all()
    serializer_class = prop_serializers.ListingPriceByPropertyCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def update(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=self.partial_update
        )
        if serializer.is_valid():
            try:
                self.perform_update(serializer)
            except Exception as e:
                return Response(
                    get_error_response_dict(message=str(e)),
                    status=status.HTTP_409_CONFLICT,
                )

        return Response(
            get_success_response_dict(data=serializer.data),
            status=status.HTTP_200_OK,
        )


# ====================== BUILDING TYPE ====================================
class BuildingTypeListCreateView(ListCreateAPIView):
    queryset = prop_models.BuildingType.objects.all()
    serializer_class = prop_serializers.BuildingTypeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class BuildingTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.BuildingType.objects.all()
    serializer_class = prop_serializers.BuildingTypeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== LAND TYPE ==========================================


class LandTypeListCreateView(ListCreateAPIView):
    queryset = prop_models.LandType.objects.all()
    serializer_class = prop_serializers.LandTypeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class LandTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.LandType.objects.all()
    serializer_class = prop_serializers.LandTypeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== PROPERTY KEY FEATURE ================================


class PropertyKeyFeatureListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyKeyFeature.objects.all()
    serializer_class = prop_serializers.PropertyKeyFeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        property_id = kwargs["pk"]
        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(message="Property not found."),
                status=status.HTTP_404_NOT_FOUND,
            )

        key_feature_serializer = self.get_serializer(data=request.data)
        key_feature_serializer.is_valid(raise_exception=True)
        key_feature_serializer.save(property=property_instance)
        return Response(
            get_success_response_dict(data=key_feature_serializer.data),
            status=status.HTTP_200_OK,
        )


class PropertyKeyFeatureRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyKeyFeature.objects.all()
    serializer_class = prop_serializers.PropertyKeyFeatureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ====================== PROPERTY IMAGE LABEL ================================


class PropertyImageLabelListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyImageLabel.objects.all()
    serializer_class = prop_serializers.PropertyImageLabelSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class PropertyImageLabelRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyImageLabel.objects.all()
    serializer_class = prop_serializers.PropertyImageLabelSerializer
    permission_classes = [IsAdminUserOrReadOnly]


# ====================== PROPERTY IMAGE ================================


class PropertyImageListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        # print("===============================>: ", request.data)
        # print(len(request.data))
        # if not "images" in request.data:
        #     return Response(
        #         {"errors": "images must be provided"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )
        # images = [request.data]
        # print("===============================>: ", images)
        property_id = kwargs["pk"]
        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(message="Property not found"),
                status=status.HTTP_404_NOT_FOUND,
            )

        # LIST OF DATA IS EXPECTED
        image_serializer = self.get_serializer(data=request.data, many=True)
        image_serializer.is_valid(raise_exception=True)

        image_serializer.save(property=property_instance)

        return Response(
            get_success_response_dict(data=image_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class PropertyImageRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyImage.objects.all()
    serializer_class = prop_serializers.PropertyImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ====================== PROPERTY VIDEO ================================


class PropertyVideoListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        property_id = kwargs["pk"]
        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(message="Property not found."),
                status=status.HTTP_404_NOT_FOUND,
            )
        # LIST OF DATA IS EXPECTED
        video_serializer = self.get_serializer(data=request.data, many=True)
        video_serializer.is_valid(raise_exception=True)
        video_serializer.save(property=property_instance)
        return Response(
            get_success_response_dict(data=video_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class PropertyVideoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyVideo.objects.all()
    serializer_class = prop_serializers.PropertyVideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ====================== PROPERTY PLAN ================================


class PropertyPlanListCreateView(ListCreateAPIView):
    queryset = prop_models.PropertyPlan.objects.all()
    serializer_class = prop_serializers.PropertyPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        property_id = kwargs["pk"]
        try:
            property_instance = prop_models.Property.objects.get(pk=property_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(message="Property not found."),
                status=status.HTTP_404_NOT_FOUND,
            )
        # LIST OF DATA IS EXPECTED
        plan_serializer = self.get_serializer(data=request.data, many=True)
        plan_serializer.is_valid(raise_exception=True)
        plan_serializer.save(property=property_instance)
        return Response(
            get_success_response_dict(data=plan_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class PropertyPlanRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.PropertyPlan.objects.all()
    serializer_class = prop_serializers.PropertyPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# ====================== PROPERTY ========================================
class PropertyCreateView(CreateAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.PropertyCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorizedAgentAdmin]
    pagination_class = GeneralCustomPagination

    def post(self, request, *args, **kwargs):
        # ALL PROPERTY RELATED DATABASE WRITE OPERATIONS, INCLUDING CHILD OBJECT SAVE, MUST BE ATOMIC
        with transaction.atomic():
            data = request.data

            # CHECK IF ADDRESS IS AVAILABLE IN INCOMING DATA, RESPOND BAD REQUEST OTEHRWISE
            if "address" not in data:
                return Response(
                    get_error_response_dict(
                        message="You must provide address of the property."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # CHECK IF SUB-PROPERTY, SUCH AS APARTMENT, VILLA, ETC. IS AVAILABLE IN INCOMING DATA, RESPOND BAD REQUEST OTEHRWISE
            if "sub_property" not in data:
                return Response(
                    get_error_response_dict(
                        message="You must add a sub-property, i.e. Apartment, Villa, etc."
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # DROP SUB-PROPERTY AND ADDRESS DATA FROM THE ORIGINAL INCOMING(REQUEST) DATA
            sub_property_data = request.data.pop("sub_property")
            address_data = request.data.pop("address")

            # DESERIALIZE ADDRESS DATA AND SAVE IF VALID
            address_serializer = AddressSerializer(data=address_data)
            if address_serializer.is_valid(raise_exception=True):
                address_instance = address_serializer.save()

            # GENERATE CUSTOM PROPERTY ID
            custom_prop_id = generate_custom_property_id()

            # RETRIEVE PROPERTY CATEGORY FROM DATABASE, OTHERWISE RESPOND 404
            try:
                property_category = prop_models.PropertyCategory.objects.get(
                    id=data["property_category"]
                )

            except ObjectDoesNotExist as odne:
                return Response(
                    get_error_response_dict(message=str(odne)),
                    status=status.HTTP_404_NOT_FOUND,
                )

            # DETERMINE THE TYPE OF PROPERTY BEING CREATED FOR ALL SUB-PROPERTIES AND STORE IN DICTIONARY
            new_property = {
                "is_apartment": property_category.cat_key == constants.APARTMENT_KEY,
                "is_villa": property_category.cat_key == constants.VILLA_KEY,
                "is_sharehouse": property_category.cat_key == constants.SHAREHOUSE_KEY,
                "is_condominium": property_category.cat_key
                == constants.CONDOMINIUM_KEY,
                "is_townhouse": property_category.cat_key == constants.TOWNHOUSE_KEY,
                "is_commercial_property": property_category.cat_key
                == constants.COMMERCIAL_PROPERTY_KEY,
                "is_venue": property_category.cat_key == constants.VENUE_KEY,
                "is_land": property_category.cat_key == constants.LAND_KEY,
            }

            # DETERMIN RESIDENTIAL TYPE OF THE PROPERTY BEING CREATED
            if (
                new_property["is_apartment"]
                or new_property["is_villa"]
                or new_property["is_sharehouse"]
                or new_property["is_condominium"]
                or new_property["is_townhouse"]
            ):
                is_residential = True
            else:
                is_residential = False

            # DESERIALIZE PARENT PROPERTY AND SAVE IF VALID
            property_serializer = self.get_serializer(data=data)

            if property_serializer.is_valid(raise_exception=True):
                try:
                    property_instance = property_serializer.save(
                        custom_prop_id=custom_prop_id,
                        is_residential=is_residential,
                        address=address_instance,
                    )
                # RESPOND WITH INTEGRITY ERROR IF UNIQUE CONSTRAINT IS VIOLATED
                except IntegrityError as ie:
                    return Response(
                        get_error_response_dict(message=str(ie)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                except Exception as e:
                    return Response(
                        get_error_response_dict(message=str(e)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            # GET THE RIGHT SERIALIZER CLASS FOR THE SUB-PROPERTY AND UNIT PROPERTIES, IF APPLICABLE
            # SET is_multi_unit TO TRUE IF PROPERTY IS MULTI-UNIT TYPE
            # SHAREHOUSE IS CONSIDERED AS MULTI UNIT AS ROOMS ARE RENTED SEPARATELY
            is_multi_unit = False
            if new_property["is_apartment"]:
                _sub_property_serializer = prop_serializers.ApartmentSerializer
                _unit_serializer = prop_serializers.ApartmentUnitSerializer
                is_multi_unit = True
            elif new_property["is_villa"]:
                _sub_property_serializer = prop_serializers.VillaSerializer
            elif new_property["is_condominium"]:
                _sub_property_serializer = prop_serializers.CondominiumSerializer
            elif new_property["is_sharehouse"]:
                _sub_property_serializer = prop_serializers.SharehouseSerializer
                _unit_serializer = prop_serializers.SharehouseRoomSerializer
                is_multi_unit = True
            elif new_property["is_townhouse"]:
                _sub_property_serializer = prop_serializers.TownhouseSerializer
            elif new_property["is_commercial_property"]:
                _sub_property_serializer = prop_serializers.CommercialPropertySerializer
                is_multi_unit = True
            elif new_property["is_venue"]:
                _sub_property_serializer = prop_serializers.VenueSerializer
            elif new_property["is_land"]:
                _sub_property_serializer = prop_serializers.LandSerializer

            unit_data = None
            # DROP THE UNITS DATA IF IT IS MULTI-UNIT PROPERTY, OTHERWISE SET EMPTY ARRAY
            if is_multi_unit:
                if "units" in sub_property_data:
                    unit_data = sub_property_data.pop("units")
                else:
                    unit_data = []
                    # return Response({"errors": {"detail": "Unit data is missed. A multi_unit property should have atleast one unit."}},
                    #                 status=status.HTTP_400_BAD_REQUEST)

            # DESERIALIZE THE SUB-PROPERTY AND SAVE IF VALID
            sub_property_serializer = _sub_property_serializer(data=sub_property_data)

            if sub_property_serializer.is_valid(raise_exception=True):
                sub_property_instance = sub_property_serializer.save(
                    parent_property=property_instance
                )

                # IF UNIT DATA AVAILABLE DESERIALIZE BASED ON UNIT SERIALIZER TYPE AND SAVE IT IF VALID
                if unit_data:
                    # CHECK IF PROPERTY IS APARTMENT OR SHAREHOUSE
                    if new_property["is_apartment"] or new_property["is_sharehouse"]:
                        unit_serializer = _unit_serializer(data=unit_data, many=True)
                        if unit_serializer.is_valid(raise_exception=True):
                            # DESERIALIZE AND SAVE APARTMENT UNIT IF UNIT IS APARTMENT UNIT
                            if new_property["is_apartment"]:
                                unit_serializer.save(apartment=sub_property_instance)

                            # DESERIALIZE AND SAVE SHAREHOUSE UNIT IF UNIT IS SHAREHOUSE UNIT
                            elif new_property["is_sharehouse"]:
                                unit_serializer.save(sharehouse=sub_property_instance)

                    # CHECK IF PROPERTY IS COMMERCIAL PROPERTY
                    elif new_property["is_commercial_property"]:
                        unit_serializer_data = {"office_units": [], "other_units": []}
                        for single_unit_data in unit_data:
                            unit_type = single_unit_data.pop("unit_type")

                            # CHECK IF UNIT IS OFFICE UNIT OR OTHER UNIT OF COMMERCIAL PROPERTY
                            if unit_type == constants.OFFICE_COMMERCIAL_PROPERTY_UNIT:
                                _unit_serializer = prop_serializers.OfficeUnitSerializer
                                unit_type_key = "office_units"
                            else:
                                _unit_serializer = (
                                    prop_serializers.OtherCommercialPropertyUnitSerializer
                                )
                                unit_type_key = "other_units"

                            # DESERIALIZE COMMERCIAL PROPERTY UNIT AND SAVE IF VALID
                            com_unit_serializer = _unit_serializer(
                                data=single_unit_data
                            )
                            if com_unit_serializer.is_valid(raise_exception=True):
                                try:
                                    com_unit_serializer.save(
                                        commercial_property=sub_property_instance
                                    )

                                    # APPEND THE COMMERCIAL PROPERTY UNIT DATA TO THE unit_serializer_data SO THAT WE
                                    # CAN USE IT LATER TO SEND BACK TO THE CLIENT
                                    unit_serializer_data[unit_type_key].append(
                                        com_unit_serializer.data
                                    )

                                # CHECK AND RESPOND ERROR IF THERE IS INTEGRITY OR OTHER ERROR
                                except IntegrityError as ie:
                                    return Response(
                                        get_error_response_dict(
                                            message=f"Integrity error. {str(ie)}"
                                        ),
                                        status=status.HTTP_409_CONFLICT,
                                    )
                                except Exception as e:
                                    return Response(
                                        get_error_response_dict(message=str(ie)),
                                        status=status.HTTP_400_BAD_REQUEST,
                                    )

                    # IF MULTI-UNIT PROPERTY IS APARTMENT OR SHAREHOUSE, CREATE LIST OF DICTIONARIES FROM LIST OF ORDERED DICT
                    # SO THAT IT CONVENIENT TO SEND THE DATA TO THE CLIENT
                    if new_property["is_apartment"] or new_property["is_sharehouse"]:
                        unit_serializer_data = [
                            dict(unit_ordered_dict)
                            for unit_ordered_dict in unit_serializer.data
                        ]

                    tasks.send_new_property_added_email_to_agent.delay(
                        custom_property_id=property_instance.custom_prop_id,
                        agent_branch=property_instance.agent_branch.id,
                    )
                    # SEND RESPONSE IF PROPERTY IS MULTI-UNIT PROPERTY
                    # INCASE OF SHAREHOUSE, UNITS = ROOMS

                    return Response(
                        get_success_response_dict(
                            message="Property created.",
                            data={
                                **property_serializer.data,
                                "sub_property": {
                                    **sub_property_serializer.data,
                                    "units": unit_serializer_data,
                                },
                                "address": {**address_serializer.data},
                            },
                        ),
                        status=status.HTTP_201_CREATED,
                    )

            tasks.send_new_property_added_email_to_agent.delay(
                custom_property_id=property_instance.custom_prop_id,
                # agent=property_instance.agent,
                agent_branch=property_instance.agent_branch.id,
            )
            # SEND RESPONSE IF PROPERTY IS NON MULTI-UNIT PROPERTY
            return Response(
                get_success_response_dict(
                    message="Property created.",
                    data={
                        **property_serializer.data,
                        "sub_property": {**sub_property_serializer.data},
                        "address": {**address_serializer.data},
                    },
                ),
                status=status.HTTP_201_CREATED,
            )


def get_property_constructed_lookup_and_order_by_params(
    request,
    own_agent=None,
    agent_in_query=None,
    own_agent_branch=None,
    agent_branch_in_query=None,
):
    """
    Construct lookup and ordering params from the url query parameters.
    The client can flexibly set query params, like:

    ?agent=23&is_residential=true

    It is possible to set all or anyone or none of the following parameters.

    ######################################
    Search params:
            - agent
            - agent_branch
            - is_residential
            - property_id
            - property_name
            - property_category => send property_category_key
            - tenure
            - tax_band
            - added_since => ie. 10_days, 24_hours, 1_week, 3_weeks, etc

    Sorting Params:
        - sort_by
    """
    q = request.query_params
    agent = agent_in_query if agent_in_query else own_agent

    agent_branch = agent_branch_in_query if agent_branch_in_query else own_agent_branch

    is_residential = get_boolean_url_query_value(request, "is_residential")

    all_lookups = []
    lookups_params = {}
    if agent:
        lookups_params["agent_branch__agent"] = agent
    if agent_branch:
        lookups_params["agent_branch"] = agent_branch
    if "property_id" in q:
        lookups_params["property_id"] = q["property_id"]
    if "custom_prop_id" in q:
        lookups_params["custom_prop_id"] = q["custom_prop_id"]
    if "property_category" in q:
        lookups_params["property_category__cat_key"] = q["property_category"]
    if "property_name" in q:
        lookups_params["name__icontains"] = q["property_name"]
    if is_residential is not None:
        lookups_params["is_residential"] = is_residential
    if "tenure" in q:
        lookups_params["tenure"] = q["tenure"]
    if "tax_band" in q:
        lookups_params["tax_band"] = q["tax_band"]

    # PROPERTY REGISTRATION DATE LOOKUP
    added_since = (
        request.query_params["added_since"]
        if "added_since" in request.query_params
        else None
    )

    # IF ADDED DATE QUERY PARAM PROVIDED
    if added_since:
        if "hour" in added_since:
            time_delta = timezone.timedelta(hours=int(added_since.split("_")[0]))
        elif "day" in added_since:
            time_delta = timezone.timedelta(days=int(added_since.split("_")[0]))
        elif "week" in added_since:
            time_delta = timezone.timedelta(weeks=int(added_since.split("_")[0]))
        lookups_params["added_on__gte"] = timezone.now() - time_delta

    q_lookup1 = Q(**lookups_params)

    all_lookups.append(q_lookup1)

    # ORDER BY
    ordering_params = request.GET.getlist("sort_by")

    return (all_lookups, ordering_params)


class PropertyListByAdminView(ListAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.ListingPropertySerializer
    permission_classes = [IsAdminUser]
    pagination_class = GeneralCustomPagination

    def get_queryset(self):
        user = self.request.user

        # CHECK IF AGENT BRANCH IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
        # IT ALLOWS TO LIST PROPERTIES FROM A SPECIFIC AGENT BRANCH
        agent_branch_in_query = None
        if "agent_branch" in self.request.query_params:
            agent_branch_in_query = self.request.query_params.get("agent_branch")

        agent_in_query = None
        if "agent" in self.request.query_params:
            agent_in_query = self.request.query_params.get("agent")

        # CONTRUCT THE LOOKUP AND ORDERING PARAMS FROM QUERY PARAMS
        (
            constructed_lookups,
            order_by,
        ) = get_property_constructed_lookup_and_order_by_params(
            self.request,
            agent_in_query=agent_in_query,
            agent_branch_in_query=agent_branch_in_query,
        )

        # FILTER THE PROPERTIES
        queryset = (
            super().get_queryset().filter(*constructed_lookups).order_by(*order_by)
        )
        return queryset


class PropertyListByAgentView(ListAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.ListingPropertySerializer
    permission_classes = [IsAgent]

    def get_queryset(self):
        # agent_id = self.kwargs["agent"]
        user = self.request.user

        # CHECK IF AGENT BRANCH IS IN QUERY PARAMS, OTHERWISE SET IT NONE IN THE LOOKUP
        # IT ALLOWS TO LIST PROPERTIES FROM A SPECIFIC AGENT BRANCH
        _agent_branch_in_query = None
        if "agent_branch" in self.request.query_params:
            _agent_branch_in_query = self.request.query_params.get("agent_branch")

        # GET THE AGENT ADMIN ASSOCIATED WITH CURRENT USER
        # IF NO AGENT ADMIN OBJECT FOUND, REPLY ERROR
        agent_admin_instance = AgentAdmin.objects.select_related(
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
        agent_branch_in_query = None

        # IF THE AGENT BRANCH THAT THE CURRENT USER IS WORKING IS A MAIN BRANCH,
        # THE USER CAN ACCESS OTHER AGENT BRANCHES PROPERTIES OF THE SAME AGENT
        # GET THE AGENT BRANCH USING THE AGENT BRANCH ID FROM QUERY PARAM AND COMPARE
        # WITH USERS OWN AGENT. IF EQUAL, THEN ADD THE AGENT BRANCH QUERY PARAM IN THE LOOKUP
        if own_agent_branch.is_main_branch and _agent_branch_in_query:
            query_agent_branch_instance = AgentBranch.objects.filter(
                id=_agent_branch_in_query
            ).first()
            if (
                query_agent_branch_instance
                and query_agent_branch_instance.agent == own_agent
            ):
                agent_branch_in_query = _agent_branch_in_query

        is_main_branch = own_agent_branch.is_main_branch

        # CONTRUCT THE LOOKUP AND ORDERING PARAMS FROM QUERY PARAMS
        (
            constructed_lookups,
            order_by,
        ) = get_property_constructed_lookup_and_order_by_params(
            self.request,
            own_agent=own_agent.id,
            own_agent_branch=None if is_main_branch else own_agent_branch.id,
            agent_branch_in_query=agent_branch_in_query,
        )

        queryset = (
            super().get_queryset().filter(*constructed_lookups).order_by(*order_by)
        )
        return queryset


# class PropertyListByAgentBranchView(ListAPIView):
#     queryset = prop_models.Property.objects.all()
#     serializer_class = prop_serializers.ListingPropertySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         agent_branch_id = self.kwargs["agent_branch"]
#         queryset = super().get_queryset().filter(agent_branch=agent_branch_id)

#         return queryset


class AdminPropertyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.ListingPropertySerializer
    permission_classes = [IsAdminUser]


class AgentPropertyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Property.objects.all()
    serializer_class = prop_serializers.ListingPropertySerializer
    permission_classes = [IsAgent, DoesAgentOwnThisProperty]

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)


# =====================APARTMENT=========================================================
class ApartmentUnitListCreateByApartmentView(ListCreateAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        apartment_id = self.kwargs["apartment_id"]
        queryset = (
            super().get_queryset().filter(apartment=apartment_id)
        )  # prop_models.ApartmentUnit.objects.filter(apartment=apartment_id)
        return queryset

    def post(self, request, *args, **kwargs):
        apartment_id = kwargs["apartment_id"]

        try:
            apartment_instance = prop_models.Apartment.objects.get(pk=apartment_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Apartment with id {apartment_id} Not Found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        apartment_unit_data = request.data
        apartment_unit_serializer = self.get_serializer(data=apartment_unit_data)
        apartment_unit_serializer.is_valid(raise_exception=True)
        apartment_unit_serializer.save(apartment=apartment_instance)

        apartment_instance.is_multi_unit = True
        apartment_instance.save()
        return Response(
            get_success_response_dict(data=apartment_unit_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class ApartmentListByAgentView(ListAPIView):
    queryset = prop_models.Apartment.objects.all()
    serializer_class = prop_serializers.ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class ApartmentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Apartment.objects.all()
    serializer_class = prop_serializers.ApartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# class ApartmentUnitCreateView(CreateAPIView):
#     queryset = prop_models.ApartmentUnit.objects.all()
#     serializer_class = prop_serializers.ApartmentUnitSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


class ApartmentUnitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.ApartmentUnit.objects.all()
    serializer_class = prop_serializers.ApartmentUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================SHAREHOUSE=========================================================
class RoomListCreateBySharehouseView(ListCreateAPIView):
    queryset = prop_models.Room.objects.all()
    serializer_class = prop_serializers.SharehouseRoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        sharehouse_id = self.kwargs["sharehouse_id"]
        queryset = super().get_queryset().filter(sharehouse=sharehouse_id)
        return queryset

    def post(self, request, *args, **kwargs):
        sharehouse_id = kwargs["sharehouse_id"]

        try:
            sharehouse_instance = prop_models.Sharehouse.objects.get(pk=sharehouse_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Sharehouse with id {sharehouse_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        room_data = request.data
        room_serializer = self.get_serializer(data=room_data)
        room_serializer.is_valid(raise_exception=True)
        room_serializer.save(sharehouse=sharehouse_instance)
        return Response(
            get_success_response_dict(data=room_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class SharehouseListByAgentView(ListAPIView):
    queryset = prop_models.Sharehouse.objects.all()
    serializer_class = prop_serializers.SharehouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class SharehouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Sharehouse.objects.all()
    serializer_class = prop_serializers.SharehouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SharehouseRoomRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Room.objects.all()
    serializer_class = prop_serializers.SharehouseRoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================VILLA=========================================================


class VillaListByAgentView(ListAPIView):
    queryset = prop_models.Villa.objects.all()
    serializer_class = prop_serializers.VillaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class VillaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Villa.objects.all()
    serializer_class = prop_serializers.VillaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================CONDOMINIUM=====================================================


class CondominiumListByAgentView(ListAPIView):
    queryset = prop_models.Condominium.objects.all()
    serializer_class = prop_serializers.CondominiumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class CondominiumRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Condominium.objects.all()
    serializer_class = prop_serializers.CondominiumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================TOWNHOUSE=====================================================


class TownhouseListByAgentView(ListAPIView):
    queryset = prop_models.Townhouse.objects.all()
    serializer_class = prop_serializers.TownhouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class TownhouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Townhouse.objects.all()
    serializer_class = prop_serializers.TownhouseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================VENUE=====================================================


class VenueListByAgentView(ListAPIView):
    queryset = prop_models.Venue.objects.all()
    serializer_class = prop_serializers.VenueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class VenueRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Venue.objects.all()
    serializer_class = prop_serializers.VenueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================LAND=====================================================


class LandListByAgentView(ListAPIView):
    queryset = prop_models.Land.objects.all()
    serializer_class = prop_serializers.LandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class LandRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.Land.objects.all()
    serializer_class = prop_serializers.LandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================COMMERCIAL PROPERTY===========================================
class OfficeListCreateByCommercialPropertyView(ListCreateAPIView):
    queryset = prop_models.OfficeUnit.objects.all()
    serializer_class = prop_serializers.OfficeUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        commercialproperty_id = self.kwargs["commercialproperty_id"]
        queryset = (
            super().get_queryset().filter(commercial_property=commercialproperty_id)
        )
        return queryset

    def post(self, request, *args, **kwargs):
        commercialproperty_id = kwargs["commercialproperty_id"]

        try:
            commercial_property_instance = prop_models.CommercialProperty.objects.get(
                pk=commercialproperty_id
            )
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Commercial Property with id {commercialproperty_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        office_unit_data = request.data
        office_unit_serializer = self.get_serializer(data=office_unit_data)
        if office_unit_serializer.is_valid():
            try:
                office_unit_serializer.save(
                    commercial_property=commercial_property_instance
                )
            except IntegrityError as ie:
                err = (
                    "Duplicate unit name or number."
                    if "duplicate key" in str(ie).lower()
                    else str(ie)
                )
                return Response(
                    get_error_response_dict(message=err),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            # IF EXCEPTION IS OTHER THAN INTEGRITY ERROR
            except Exception as exc:
                return Response(
                    get_error_response_dict(message=str(exc)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            get_success_response_dict(data=office_unit_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class OtherUnitListCreateByCommercialPropertyView(ListCreateAPIView):
    queryset = prop_models.OtherCommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.OtherCommercialPropertyUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        commercialproperty_id = self.kwargs["commercialproperty_id"]
        queryset = (
            super().get_queryset().filter(commercial_property=commercialproperty_id)
        )
        return queryset

    def post(self, request, *args, **kwargs):
        commercialproperty_id = kwargs["commercialproperty_id"]

        try:
            commercial_property_instance = prop_models.CommercialProperty.objects.get(
                pk=commercialproperty_id
            )
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Commercial Property with id {commercialproperty_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        other_unit_data = request.data
        other_unit_serializer = self.get_serializer(data=other_unit_data)
        if other_unit_serializer.is_valid():
            try:
                other_unit_serializer.save(
                    commercial_property=commercial_property_instance
                )
            except IntegrityError as ie:
                err = (
                    "Duplicate unit name or number."
                    if "duplicate key" in str(ie).lower()
                    else str(ie)
                )
                return Response(
                    get_error_response_dict(message=err),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            # IF EXCEPTION IS OTHER THAN INTEGRITY ERROR
            except Exception as exc:
                return Response(
                    get_error_response_dict(message=str(exc)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            get_success_response_dict(data=other_unit_serializer.data),
            status=status.HTTP_201_CREATED,
        )


class CommercialPropertyListByAgentView(ListAPIView):
    queryset = prop_models.CommercialProperty.objects.all()
    serializer_class = prop_serializers.CommercialPropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = super().get_queryset().filter(parent_property__agent=agent_id)
        return queryset


class CommercialPropertyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.CommercialProperty.objects.all()
    serializer_class = prop_serializers.CommercialPropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OfficeListByAgentView(ListAPIView):
    queryset = prop_models.OfficeUnit.objects.all()
    serializer_class = prop_serializers.OfficeUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = (
            super()
            .get_queryset()
            .filter(commercial_property__parent_property__agent=agent_id)
        )
        return queryset


class OfficeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = prop_models.OfficeUnit.objects.all()
    serializer_class = prop_serializers.OfficeUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OtherComemrcialPropertyUnitListByAgentView(ListAPIView):
    queryset = prop_models.OtherCommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.OtherCommercialPropertyUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        agent_id = self.kwargs["agent_id"]
        queryset = (
            super()
            .get_queryset()
            .filter(commercial_property__parent_property__agent=agent_id)
        )
        return queryset


class OtherCommercialPropertyUnitRetrieveUpdateDestroyView(
    RetrieveUpdateDestroyAPIView
):
    queryset = prop_models.OtherCommercialPropertyUnit.objects.all()
    serializer_class = prop_serializers.OtherCommercialPropertyUnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# =====================PROPERTY CATEGORY AMENITY==================================
# LIST PROPERTY AMENITIES BY PROPERTY CATEGORY
class PropertyCategoryAmenityCreateListView(ListCreateAPIView):
    queryset = prop_models.PropertyCategoryAmenity.objects.all()
    serializer_class = prop_serializers.PropertyCategoryAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        property_category_id = self.kwargs["property_category_id"]
        queryset = super().get_queryset().filter(property_category=property_category_id)
        return queryset

    def post(self, request, *args, **kwargs):
        property_category_id = kwargs["property_category_id"]

        # CHECK IF REQUEST DATA IS RECIEVED WITH 'AMENITIIES' ATTRIBUTE
        if not "amenities" in request.data:
            return Response(
                get_error_response_dict(message="List of amenities not provided."),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CLIENT IS EXPECTED TO SEND LIST OF AMENITIES
        amenities = request.data["amenities"]

        # CHECK IF LIST OF AMENITIES ARE RECIEVED FROM CLIENT
        if type(amenities).__name__ != "list":
            return Response(
                get_error_response_dict(
                    message=f"List of amenities expected. Got {type(amenities).__name__}"
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            # GET PROPERTY CATEGORY INSTANCE FROM DB
            property_category_instance = prop_models.PropertyCategory.objects.get(
                id=property_category_id
            )
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Property category with id {property_category_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CHANGE LIST OF AMENITIES ID TO LIST OF DICTIONARIES AS [{"amenities": 2}...]
        amenities_with_dict = [{"amenity": amenity} for amenity in amenities]
        property_category_amenity_serializer = self.get_serializer(
            data=amenities_with_dict, many=True
        )
        if property_category_amenity_serializer.is_valid():
            try:
                # .save WILL DO BULK SAVE
                property_category_amenity_serializer.save(
                    property_category=property_category_instance
                )
            # CAPTURE DUPLICATE SAVE
            except IntegrityError as ie:
                return Response(
                    get_error_response_dict(message=str(ie)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                get_success_response_dict(
                    data=property_category_amenity_serializer.data
                ),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(
                    message=property_category_amenity_serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class PropertyCategoryAmenityRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = prop_models.PropertyCategoryAmenity.objects.all()
    serializer_class = prop_serializers.PropertyCategoryAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_url_kwarg = "property_category_amenity_id"


# =====================PROPERTY AMENITY===========================================
# LIST/CREATE PROPERTY AMENITIES BY PROPERTY
class PropertyAmenityCreateListView(ListCreateAPIView):
    queryset = prop_models.PropertyAmenity.objects.all()
    serializer_class = prop_serializers.PropertyAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        property_id = self.kwargs["property_id"]
        queryset = super().get_queryset().filter(parent_property=property_id)
        return queryset

    def post(self, request, *args, **kwargs):
        property_id = kwargs["property_id"]

        # CHECK IF REQUEST DATA IS RECIEVED WITH 'AMENITIIES' ATTRIBUTE
        if not "amenities" in request.data:
            return Response(
                get_error_response_dict(message=f"List of amenities must be provided."),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CLIENT IS EXPECTED TO SEND LIST OF AMENITIES
        amenities = request.data["amenities"]

        # CHECK IF LIST OF AMENITIES ARE RECIEVED FROM CLIENT
        if type(amenities).__name__ != "list":
            return Response(
                get_error_response_dict(
                    message=f"List of amenities expected. Got {type(amenities).__name__}"
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            # GET PROPERTY INSTANCE FROM DB
            property_instance = prop_models.Property.objects.get(id=property_id)
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Property with id {property_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # GET SET OF AMENITIES FOR PROPERTY CATEGORY OF CURRENT PROPERTY
        # A PROPERTY CAN ONLY ADD AMENITIES THAT ARE LINKED TO THE PROPERTY CATEGORY
        priperty_category_amenities_set = property_instance.property_category.propertycategoryamenity_set.all().values_list(
            "amenity", flat=True
        )

        # CHANGE THE RECIEVED AMENITIES LIST TO SET
        amenities_set = set(amenities)

        # CHECK IF ALL RECIEVED AMENITIES ARE LINKED TO PROPERTY CATEGORY
        # OTHERWISE RETURN ERROR
        if not amenities_set.issubset(priperty_category_amenities_set):
            diff = amenities_set.difference(priperty_category_amenities_set)
            return Response(
                get_error_response_dict(
                    message=f"Amenities with id: {diff} are not linked to the property category. \
                    Property amenities must be selected from amenities that are linked to the property category."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CHANGE LIST OF AMENITIES ID TO LIST OF DICTIONARIES AS [{"amenities": 2}...]
        amenities_with_dict = [{"amenity": amenity} for amenity in amenities]
        property_amenity_serializer = self.get_serializer(
            data=amenities_with_dict, many=True
        )
        if property_amenity_serializer.is_valid():
            try:
                # .save WILL DO BULK SAVE
                property_amenity_serializer.save(parent_property=property_instance)
            # CAPTURE DUPLICATE SAVE
            except IntegrityError as ie:
                return Response(
                    get_error_response_dict(message=str(ie)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                get_success_response_dict(data=property_amenity_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(message=property_amenity_serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )


# =====================APARTMENT UNIT AMENITY=====================================
# LIST/CREATE APARTMENT UNIT BY PROPERTY
class ApartmentUnitAmenityCreateListView(ListCreateAPIView):
    queryset = prop_models.ApartmentUnitAmenity.objects.all()
    serializer_class = prop_serializers.ApartmentUnitAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        apartmentunit_id = self.kwargs["apartmentunit_id"]
        queryset = super().get_queryset().filter(apartment_unit=apartmentunit_id)
        return queryset

    def post(self, request, *args, **kwargs):
        apartmentunit_id = self.kwargs["apartmentunit_id"]

        # CHECK IF REQUEST DATA IS RECIEVED WITH 'AMENITIIES' ATTRIBUTE
        if not "amenities" in request.data:
            return Response(
                get_error_response_dict(message="List of amenities not provided."),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CLIENT IS EXPECTED TO SEND LIST OF AMENITIES
        amenities = request.data["amenities"]

        # CHECK IF AMENITIES ARE RECIEVED FROM CLIENT IN LIST DATA STRUCTURE
        if type(amenities).__name__ != "list":
            return Response(
                get_error_response_dict(
                    message=f"List of amenities expected. Got {type(amenities).__name__}"
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            # GET PROPERTY INSTANCE FROM DB
            apartment_unit_instance = prop_models.ApartmentUnit.objects.get(
                id=apartmentunit_id
            )
            property_instance = apartment_unit_instance.apartment.parent_property
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Apartment Unit with id {apartmentunit_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # GET SET OF AMENITIES FOR PROPERTY CATEGORY OF CURRENT PROPERTY
        # AN APARTMENTUNIT CAN ONLY ADD AMENITIES THAT ARE LINKED TO THE PROPERTY CATEGORY
        priperty_category_amenities_set = property_instance.property_category.propertycategoryamenity_set.all().values_list(
            "amenity", flat=True
        )

        # CHANGE THE RECIEVED AMENITIES LIST TO SET
        amenities_set = set(amenities)

        # CHECK IF ALL RECIEVED AMENITIES ARE LINKED TO PROPERTY CATEGORY
        # OTHERWISE RETURN ERROR
        if not amenities_set.issubset(priperty_category_amenities_set):
            diff = amenities_set.difference(priperty_category_amenities_set)
            return Response(
                get_error_response_dict(
                    message=f"Amenities with ids: {diff} are not linked to the property category \
                        Property amenities must be selected from amenities that are linked to the property category."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CHANGE LIST OF AMENITIES ID TO LIST OF DICTIONARIES AS [{"amenities": 2}...]
        amenities_with_dict = [{"amenity": amenity} for amenity in amenities]
        apartment_unit_amenity_serializer = self.get_serializer(
            data=amenities_with_dict, many=True
        )
        if apartment_unit_amenity_serializer.is_valid():
            try:
                # .save WILL DO BULK SAVE
                apartment_unit_amenity_serializer.save(
                    apartment_unit=apartment_unit_instance
                )
            # CAPTURE DUPLICATE SAVE
            except IntegrityError as ie:
                return Response(
                    get_error_response_dict(message=str(ie)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                get_success_response_dict(data=apartment_unit_amenity_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(
                    message=apartment_unit_amenity_serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


# =====================OFFICE UNIT AMENITY=====================================
# LIST/CREATE OFFICE UNIT BY PROPERTY
class OfficeUnitAmenityCreateListView(ListCreateAPIView):
    queryset = prop_models.OfficeUnitAmenity.objects.all()
    serializer_class = prop_serializers.OfficeUnitAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        officeunit_id = self.kwargs["officeunit_id"]
        queryset = super().get_queryset().filter(office_unit=officeunit_id)
        return queryset

    def post(self, request, *args, **kwargs):
        officeunit_id = self.kwargs["officeunit_id"]

        # CHECK IF REQUEST DATA IS RECIEVED WITH 'AMENITIIES' ATTRIBUTE
        if not "amenities" in request.data:
            return Response(
                get_error_response_dict(message="List of amenities not provided."),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CLIENT IS EXPECTED TO SEND LIST OF AMENITIES
        amenities = request.data["amenities"]

        # CHECK IF AMENITIES ARE RECIEVED FROM CLIENT IN LIST DATA STRUCTURE
        if type(amenities).__name__ != "list":
            return Response(
                get_error_response_dict(
                    message=f"List of amenities expected. Got {type(amenities).__name__}"
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            # GET PROPERTY INSTANCE FROM DB
            office_unit_instance = prop_models.OfficeUnit.objects.get(id=officeunit_id)
            property_instance = office_unit_instance.commercial_property.parent_property
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Office Unit with id {officeunit_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # GET SET OF AMENITIES FOR PROPERTY CATEGORY OF CURRENT PROPERTY
        # AN OFFICEUNIT CAN ONLY ADD AMENITIES THAT ARE LINKED TO THE PROPERTY CATEGORY
        priperty_category_amenities_set = property_instance.property_category.propertycategoryamenity_set.all().values_list(
            "amenity", flat=True
        )

        # CHANGE THE RECIEVED AMENITIES LIST TO SET
        amenities_set = set(amenities)

        # CHECK IF ALL RECIEVED AMENITIES ARE LINKED TO PROPERTY CATEGORY
        # OTHERWISE RETURN ERROR
        if not amenities_set.issubset(priperty_category_amenities_set):
            diff = amenities_set.difference(priperty_category_amenities_set)
            return Response(
                get_error_response_dict(
                    message=f"Amenities with id: {diff} are not linked to the property category. \
                        Office unit amenities must be selected from amenities that are linked to the property category."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CHANGE LIST OF AMENITIES ID TO LIST OF DICTIONARIES AS [{"amenities": 2}...]
        amenities_with_dict = [{"amenity": amenity} for amenity in amenities]
        office_unit_amenity_serializer = self.get_serializer(
            data=amenities_with_dict, many=True
        )
        if office_unit_amenity_serializer.is_valid():
            try:
                # .save WILL DO BULK SAVE
                office_unit_amenity_serializer.save(office_unit=office_unit_instance)
            # CAPTURE DUPLICATE SAVE
            except IntegrityError as ie:
                return Response(
                    get_error_response_dict(message=str(ie)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                get_success_response_dict(data=office_unit_amenity_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(message=office_unit_amenity_serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )


# =====================OTHER COMMERCIAL PROPERTY UNIT AMENITY=============================
# LIST/CREATE OTHER COMMERCIAL PROPERTY UNIT BY PROPERTY
class OtherCommercialPropertyUnitAmenityCreateListView(ListCreateAPIView):
    queryset = prop_models.OtherCommercialPropertyUnitAmenity.objects.all()
    serializer_class = prop_serializers.OtherCommercialPropertyUnitAmenitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        otherunit_id = self.kwargs["othercommercialpropertyunits_id"]
        queryset = (
            super().get_queryset().filter(other_commercial_property_unit=otherunit_id)
        )
        return queryset

    def post(self, request, *args, **kwargs):
        otherunit_id = self.kwargs["othercommercialpropertyunits_id"]

        # CHECK IF REQUEST DATA IS RECIEVED WITH 'AMENITIIES' ATTRIBUTE
        if not "amenities" in request.data:
            return Response(
                get_error_response_dict(message="List of amenities not provided."),
                status=status.HTTP_404_NOT_FOUND,
            )

        # CLIENT IS EXPECTED TO SEND LIST OF AMENITIES
        amenities = request.data["amenities"]

        # CHECK IF AMENITIES ARE RECIEVED FROM CLIENT IN LIST DATA STRUCTURE
        if type(amenities).__name__ != "list":
            return Response(
                get_error_response_dict(
                    message=f"List of amenities expected. Got {type(amenities).__name__}"
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            # GET PROPERTY INSTANCE FROM DB
            other_unit_instance = prop_models.OtherCommercialPropertyUnit.objects.get(
                id=otherunit_id
            )
            property_instance = other_unit_instance.commercial_property.parent_property
        except ObjectDoesNotExist:
            return Response(
                get_error_response_dict(
                    message=f"Other Commercial Property Unit with id {otherunit_id} not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # GET SET OF AMENITIES FOR PROPERTY CATEGORY OF CURRENT PROPERTY
        # AN OFFICEUNIT CAN ONLY ADD AMENITIES THAT ARE LINKED TO THE PROPERTY CATEGORY
        property_category_amenities_set = property_instance.property_category.propertycategoryamenity_set.all().values_list(
            "amenity", flat=True
        )

        # CHANGE THE RECIEVED AMENITIES LIST TO SET
        amenities_set = set(amenities)

        # CHECK IF ALL RECIEVED AMENITIES ARE LINKED TO PROPERTY CATEGORY
        # OTHERWISE RETURN ERROR
        if not amenities_set.issubset(property_category_amenities_set):
            diff = amenities_set.difference(property_category_amenities_set)
            return Response(
                get_error_response_dict(
                    message=f"Amenities with ids: {diff} are not linked to the property category \
                        Other commercial property unit amenities must be selected from amenities that are linked to the property category."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # CHANGE LIST OF AMENITIES ID TO LIST OF DICTIONARIES AS [{"amenities": 2}...]
        amenities_with_dict = [{"amenity": amenity} for amenity in amenities]
        other_unit_amenity_serializer = self.get_serializer(
            data=amenities_with_dict, many=True
        )
        if other_unit_amenity_serializer.is_valid():
            try:
                # .save WILL DO BULK SAVE
                other_unit_amenity_serializer.save(
                    other_commercial_property_unit=other_unit_instance
                )
            # CAPTURE DUPLICATE SAVE
            except IntegrityError as ie:
                return Response(
                    get_error_response_dict(message=str(ie)),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                get_success_response_dict(data=other_unit_amenity_serializer.data),
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                get_error_response_dict(message=other_unit_amenity_serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )
