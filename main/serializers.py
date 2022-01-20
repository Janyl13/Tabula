from django.db.models import Avg
from rest_framework import serializers

from main.models import Category, Photo, Review, Likes, Rating, Favourite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    published = serializers.DateTimeField(format='%d:%m:%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Photo
        fields = ('id', 'title', 'category', 'image', 'price', 'published')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photographer'] = instance.photographer.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['review'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['photographer_id'] = user_id
        photo = Photo.objects.create(**validated_data)
        return photo

class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'category', 'photographer']


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    photographer = serializers.ReadOnlyField(source='photographer.email')

    class Meta:
        model = Review
        fields = '__all__'


    def create(self, validated_data):
        request = self.context.get('request')
        photographer = request.user
        review = Review.objects.create(photographer=photographer, **validated_data)
        return review


class LikesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    photographer = serializers.ReadOnlyField(source='photographer.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        photographer = request.user
        photo = validated_data.get('photo')
        like = Likes.objects.get_or_create(photographer=photographer, photo=photo)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class RatingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    photographer = serializers.ReadOnlyField(source='photographer.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        photographer = request.user
        photo = validated_data.get('photo')
        rating = Rating.objects.get_or_create(photographer=photographer, photo=photo)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['photographer'] = instance.photographer.email
        representation['photo'] = instance.photo.title
        return representation