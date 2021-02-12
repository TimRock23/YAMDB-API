from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                basename='reviews')
router.register(r'(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                views.CommentViewSet, basename='comments')

app_name = 'review'

urlpatterns = [
    path('v1/titles/', include(router.urls))
]
