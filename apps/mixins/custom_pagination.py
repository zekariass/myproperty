from rest_framework.pagination import LimitOffsetPagination
from apps.system.models import SystemParameter


class GeneralCustomPagination(LimitOffsetPagination):
    try:
        _page_limit = (
            SystemParameter.objects.filter(name="NUMBER_OF_ITEMS_PER_PAGE")
            .first()
            .value
        )
    except Exception:
        _page_limit = 5
    default_limit = int(_page_limit) if _page_limit else 3
