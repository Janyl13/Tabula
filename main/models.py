from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.admin import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


PRICE_CHOICES = (
    (0, '0$'),
    (1, '1$'),
    (2, '2$'),
    (3, '3$'),
    (4, '4$'),
    (5, '5$')
)

class Photo(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(null=False, blank=False, upload_to='photos')
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    price = models.IntegerField(choices=PRICE_CHOICES)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# RATING_CHOICES = (
#     (1, '1'),
#     (2, '2'),
#     (3, '3'),
#     (4, '4'),
#     (5, '5')
# )


class Review(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='reviews')
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    # rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)


class Rating(models.Model):
    photographer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='rating')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating) + " | " + self.photo.title + " | " + str(self.photographer)


class Favourite(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='favourites')
    photographer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=True)