# from rest_framework import viewsets
# from django.contrib.auth.models import User
# from http.client import responses
from collections import OrderedDict
from api.serializers import CommentSerializer, PostListSerializer, PostRetrieveSerializer, PostSerializerDetail, UserSerializer, CategorySerializer, TagSerializer, CateTagSerializer
from api.utils import obj_to_comment, obj_to_post, prev_next_post
from blog.models import Category, Comment, Post, Tag    
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import  ModelViewSet


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

# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer



# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostRetrieveSerializer # 모든필드
# 클래스 내 코드는 위 클래스와 동일하지만 상속받는 뷰가 다르므로 로직 다름
# postviewset이 하나로 코딩했었으나, 이제 2개로 나누어 로직 따로 코딩됨

# class CommentCreateAPIView(CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# patch 메서드
# class PostLikeAPIView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostLikeSerializer # 5개 필드

#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data = {'like': instance.like + 1} # 딕셔너리 기반
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response(data['like'])
    


    

    

class CateTagAPIView(APIView):
    def get(self, request, *args, **kwargs):
        cateList = Category.objects.all()
        tagList = Tag.objects.all()

        data = {
            'cateList': cateList,
            'tagList': tagList,
        }
        serializer = CateTagSerializer(instance=data)

        return Response(serializer.data)

    
    
class PostPageNumberPagination(PageNumberPagination):
    page_size = 3
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('postList', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
        ]))


# class PostListAPIView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostListSerializer
#     pagination_class = PostPageNumberPagination

#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }


def get_prev_next(instance):
    try:
        prev = instance.get_previous_by_update_dt()
    except instance.DoesNotExist:
        prev = None 
    
    try:
        next_ = instance.get_next_by_update_dt()
    except instance.DoesNotExist:
        next_ = None
    return prev, next_

# class PostRetrieveAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializerDetail # 모든필드

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         prevInstance, nextInstance = get_prev_next(instance)
#         commentList = instance.comment_set.all()


#         data = {
#             'post': instance,
#             'prevPost': prevInstance,
#             'nextPost': nextInstance,
#             'commentList': commentList,
#         }
#         serializer = self.get_serializer(instance=data)
#         return Response(serializer.data)
    
#     def get_serializer_context(self):
#         """
#         Extra context provided to the serializer class.
#         """
#         return {
#             'request': None,
#             'format': self.format_kwarg,
#             'view': self
#         }

# # patch 메서드
# class PostLikeAPIView(GenericAPIView):
#     queryset = Post.objects.all()
#     # serializer_class = PostLikeSerializer # 5개 필드

#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.like += 1
#         instance.save()
       
#         return Response(instance.like)
    

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostPageNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
    def get_queryset(self):
        return Post.objects.all().select_related('category').prefetch_related('tags', 'comment_set')
    

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # prevInstance, nextInstance = get_prev_next(instance)
        commentList = instance.comment_set.all()

        postDict = obj_to_post(instance)
        prevDict, nextDict = prev_next_post(instance)
        commentDict = [obj_to_comment(c) for c in commentList]

        dataDict = {
            'post': postDict,
            'prevPost': prevDict,
            'nextPost': nextDict,
            'commentList': commentDict,
        }

        return Response(dataDict)

    
    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.like += 1
        instance.save()
       
        return Response(instance.like)
    


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
