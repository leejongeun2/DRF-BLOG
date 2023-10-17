from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Category, Comment, Post, Tag  

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class PostListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = Post
        # fields = '__all__' # 클라이언트에게 보내줄 필드
        fields = ['id', 'title', 'image', 'like', 'category']
        # 출력 포맷, 출력 내용에 관한 것은 모두 serializer에서 코딩

class PostRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        # fields = '__all__' # 클라이언트에게 보내줄 필드
        exclude = ['create_dt']
        # 출력 포맷, 출력 내용에 관한 것은 모두 serializer에서 코딩


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__' # 클라이언트에게 보내줄 필드


# class PostLikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         # fields = '__all__' # 클라이언트에게 보내줄 필드
#         fields = ['like']
#         # 출력 포맷, 출력 내용에 관한 것은 모두 serializer에서 코딩


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

# class CateTagSerializer(serializers.Serializer):
#     cateList = CategorySerializer(many=True)
#     tagList = TagSerializer(many=True)

class CateTagSerializer(serializers.Serializer):
    cateList = serializers.ListField(child=serializers.CharField())
    tagList = serializers.ListField(child=serializers.CharField())

class PostSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title']

class CommentSerializerSub(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'update_dt']


class PostSerializerDetail(serializers.Serializer):
    post = PostRetrieveSerializer()
    prevPost = PostSerializerSub()
    nextPost = PostSerializerSub()
    commentList = CommentSerializerSub(many=True)
