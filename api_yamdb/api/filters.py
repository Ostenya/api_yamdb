import django_filters
from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters.ModelChoiceFilter(field_name="genre",
                                             to_field_name='slug',
                                             queryset=Genre.objects.all()
                                             )
    category = django_filters.ModelChoiceFilter(field_name="category",
                                                to_field_name='slug',
                                                queryset=Category.objects.all()
                                                )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category',)
