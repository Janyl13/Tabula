from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    CreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.filters import PhotoFilter
from main.models import Category, Photo, Review, Favourite, Likes, Rating
from main.permissions import IsPhotographer
from main.serializers import CategorySerializer, PhotoSerializer, PhotoListSerializer, ReviewSerializer, \
    LikesSerializer, RatingSerializer


# class PermissionMixin:
#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             permissions = [IsAdminUser, ]
#         else:
#             permissions = [IsAuthenticated, ]
#         return [permission() for permission in permissions]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    permission_classes = [AllowAny, ]


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    queryset_any = Favourite.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'category__name']
    filterset_class = PhotoFilter
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == 'list':
            return PhotoListSerializer
        return PhotoSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def filter(self, request, pk=None):
        queryset = self.get_queryset()
        start_date = timezone.now() - timedelta(days=1)
        queryset = queryset.filter(created_at__gte=start_date)
        serializer = PhotoSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(category__iname=q))
        serializer = PhotoSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def favourite(self, request, pk=None):
        photo = self.get_object()
        obj, created = Favourite.objects.get_or_create(photographer=request.user, photo=photo, )
        if not created:
            obj.favourite = not obj.favourite
            obj.save()
        favourites = 'added to favourites' if obj.favourite else 'removed to favourites'
        return Response('Successfully {} !'.format(favourites), status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsPhotographer, ]


class LikesViewSet(ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsPhotographer, ]


class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsPhotographer, ]



