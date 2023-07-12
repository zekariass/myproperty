from rest_framework.pagination import LimitOffsetPagination
from apps.system.models import SystemParameter


class GeneralCustomPagination(LimitOffsetPagination):
    _page_limit = (
        SystemParameter.objects.filter(name="NUMBER_OF_ITEMS_PER_PAGE").first().value
    )
    default_limit = int(_page_limit) if _page_limit else 3
