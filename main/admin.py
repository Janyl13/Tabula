from django.contrib import admin

from main.models import Category, Photo, Review, Likes, Rating

admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Review)
admin.site.register(Likes)
admin.site.register(Rating)


