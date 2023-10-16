# from rest_framework import viewsets
# from django.contrib.auth.models import User
# from http.client import responses
from api.serializers import CommentSerializer, PostLikeSerializer, PostListSerializer, PostRetrieveSerializer, UserSerializer
from blog.models import Comment, Post    
from rest_framework.response import Response

# class UserViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class PostViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class CommentViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveSerializer # 모든필드
# 클래스 내 코드는 위 클래스와 동일하지만 상속받는 뷰가 다르므로 로직 다름
# postviewset이 하나로 코딩했었으나, 이제 2개로 나누어 로직 따로 코딩됨

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class PostLikeAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer # 5개 필드

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = {'like': instance.like + 1} # 딕셔너리 기반
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data['like'])
