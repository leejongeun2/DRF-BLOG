from django.urls import path, include
from rest_framework import routers
from api.views import PostViewSet, UserViewSet

router = routers.DefaultRouter() # DefaultRouter 사용, users는 get, post 가능 pk는 get, put, delete, patch 이 라우터에 의해 만들어짐
router.register(r'user', UserViewSet)
router.register(r'post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
