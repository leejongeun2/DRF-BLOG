# ViewSets define the view behavior.

from rest_framework import viewsets
from django.contrib.auth.models import User
from api.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet): # modelviewset을 상속받았기 때문에 user에 대한 crud가능
    queryset = User.objects.all()
    serializer_class = UserSerializer