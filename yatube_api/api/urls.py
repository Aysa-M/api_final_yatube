from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView,
                                            TokenVerifyView)
from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
router_v1.register(r'groups', GroupViewSet, basename='groups')
router_v1.register(r'follow', FollowViewSet, basename='followings')

urlpatterns = [
    path('v1/jwt/create/', TokenObtainPairView.as_view()),
    path('v1/jwt/refresh/', TokenRefreshView.as_view()),
    path('v1/jwt/verify/', TokenVerifyView.as_view()),
    path('v1/', include(router_v1.urls)),
]
