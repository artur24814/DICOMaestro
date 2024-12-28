import django_filters
from django.utils.timezone import now
from .models import DeveloperActivityLog


class DeveloperActivityLogFilter(django_filters.FilterSet):
    timestamp__year = django_filters.NumberFilter(
        field_name='timestamp__year',
        lookup_expr='exact',
        method='filter_year',
        label='Year'
    )
    timestamp__month = django_filters.NumberFilter(
        field_name='timestamp__month',
        lookup_expr='exact',
        method='filter_month',
        label='Month'
    )

    class Meta:
        model = DeveloperActivityLog
        fields = ['timestamp__year', 'timestamp__month']

    def filter_year(self, queryset, name, value):
        if value is None:
            value = now().year
        return queryset.filter(timestamp__year=value)

    def filter_month(self, queryset, name, value):
        if value is None:
            value = now().month
        return queryset.filter(timestamp__month=value)
