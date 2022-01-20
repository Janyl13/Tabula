from django_filters import rest_framework as filters

from main.models import Photo


class PhotoFilter(filters.FilterSet):
    price_from = filters.NumberFilter(field_name='price',
                                      lookup_expr='gte')
    price_to = filters.NumberFilter(field_name='price',
                                    lookup_expr='lte')
    class Meta:
        model = Photo
        fields = ['category']