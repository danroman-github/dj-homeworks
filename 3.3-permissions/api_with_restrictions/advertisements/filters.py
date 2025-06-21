from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter()
    status = filters.CharFilter(lookup_expr='iexact')
    creator = filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at']
