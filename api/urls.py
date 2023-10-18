# from django.urls import path, include
# from rest_framework import routers
# from api.views import CommentViewSet, PostViewSet, UserViewSet

# router = routers.DefaultRouter() # DefaultRouter 사용, users는 get, post 가능 pk는 get, put, delete, patch 이 라우터에 의해 만들어짐
# router.register(r'user', UserViewSet)
# router.register(r'post', PostViewSet)
# router.register(r'comment', CommentViewSet) # url 프리픽스

# urlpatterns = [
#     path('', include(router.urls)),
# ]


from django.urls import path
from api import views

urlpatterns = [
    # path('post/', views.PostListAPIView.as_view(), name='post-list'),
    # path('post/<int:pk>/', views.PostRetrieveAPIView.as_view(), name='post-detail'),
    # path('comment/', views.CommentCreateAPIView.as_view(), name='commentt-list'),
    # path('post/<int:pk>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    # path('catetag/', views.CateTagAPIView.as_view(), name='catetag'),

    path('post/', views.PostViewSet.as_view(actions={'get': 'list',}), name='post-list'),
    path('post/<int:pk>/', views.PostViewSet.as_view(actions={'get': 'retrieve',}), name='post-detail'),
    path('comment/', views.CommentViewSet.as_view(actions={'post': 'create',}), name='commentt-list'),
    path('post/<int:pk>/like/', views.PostViewSet.as_view(actions={'get':'like',}), name='post-like'),
    path('catetag/', views.CateTagAPIView.as_view(), name='catetag'),

]