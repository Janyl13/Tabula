from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from main.views import *

schema_view = get_schema_view(
    openapi.Info(
        title='Tabula Rasa',
        description='Project',
        default_version='v1'
    ),
    public=True
)

router = DefaultRouter()
router.register('photo', PhotoViewSet, 'photos')
router.register('reviews', ReviewViewSet)
router.register('likes', LikesViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/photo/', PhotoListView.as_view()),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/docs/', schema_view.with_ui('swagger')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)