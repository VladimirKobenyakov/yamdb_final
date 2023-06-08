from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Category
        write_only_fields = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор для жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        write_only_fields = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор для произведений."""

    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(), many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate(self, attrs):
        try:
            if attrs['genre'] == []:
                raise serializers.ValidationError('Выберите '
                                                  'из существующих жанров')
            if attrs['year'] > datetime.today().year:
                raise serializers.ValidationError('Год '
                                                  'не может '
                                                  'быть больше текущего')
        except KeyError:
            pass
        return attrs


class TitleGetSerializer(serializers.ModelSerializer):
    """ Сериализатор для произведений."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('__all__')
        read_only_fields = ('rating',)
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        )
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method != 'POST':
            return data

        if Review.objects.filter(
                author=request.user,
                title=title).exists():
            raise serializers.ValidationError(
                'Нельзя сделать 2 отзыва на одно произведение!'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
