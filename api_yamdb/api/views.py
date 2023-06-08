from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title
from user.permissions import IsAdminModeratorOrReadOnly, IsAdminOrReadOnly

from .filters import PostFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleGetSerializer, TitleSerializer)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """ Класс для добавления и отображения произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGetSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """ Класс для добавления и отображения категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_serializer_context(self, *args, **kwargs):
        try:
            if self.kwargs['slug']:
                raise MethodNotAllowed(method='GET', detail=None, code=None)
        except KeyError:
            pass


class GenreViewSet(CreateListDestroyViewSet):
    """ Класс для добавления и отображения жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = [IsAdminOrReadOnly, ]
    search_fields = ('name', 'slug')
    filterset_fields = ('slug',)
    lookup_field = 'slug'

    def get_serializer_context(self, *args, **kwargs):
        try:
            if self.kwargs['slug']:
                raise MethodNotAllowed(method='GET', detail=None, code=None)
        except KeyError:
            pass


class ReviewViewSet(viewsets.ModelViewSet):
    """ Класс для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ Класс для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
