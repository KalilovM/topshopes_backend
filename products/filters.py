from django_filters.rest_framework import RangeFilter, FilterSet
import django_filters
from .models import Product, Brand


class ProductFilter(FilterSet):
		price = RangeFilter()
		brand = django_filters.ModelMultipleChoiceFilter(
				queryset=Brand.objects.all(),
				widget=django_filters.widgets.CSVWidget,
		)
		class Meta:
				model = Product
				fields = ['price', 'brand']