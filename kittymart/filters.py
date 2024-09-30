import django_filters
from kittymart.models import Kitten


class KittenFilter(django_filters.FilterSet):

    color = django_filters.ChoiceFilter(choices=Kitten.COLOR_CHOICES)


    min_age = django_filters.NumberFilter(field_name='age_in_months', lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name='age_in_months', lookup_expr='lte')

    class Meta:
        model = Kitten
        fields = ['color', 'min_age', 'max_age']
