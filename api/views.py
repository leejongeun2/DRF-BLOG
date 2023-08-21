from rest_framework import viewsets
from django.contrib.auth.models import User
from api.serializers import PostSerializer, UserSerializer
from blog.models import Post    

class UserViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
    queryset = Post.objects.all()
    serializer_class = PostSerializer