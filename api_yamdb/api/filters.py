from django_filters import CharFilter, rest_framework

from reviews.models import Title


class PostFilter(rest_framework.FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']
