from .models import Lesson, User, UserDetail, School, SchoolOwner
#from django.contrib.auth.models import User
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import LessonSerializer, UserSerializer, UserDetailSerializer, SignUpSerializer, SchoolSerializer
from .serializers import SchoolOwnerSerializer
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


#@api_view(('GET',))
#def api_root(request, format=None):
#    return Response({
#        'users': reverse('user-list', request=request, format=format),
#        'lessons': reverse('lesson-list', request=request, format=format)
#    })

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class SchoolOwnerViewSet(viewsets.ModelViewSet):
    queryset = SchoolOwner.objects.all()
    serializer_class = SchoolOwnerSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    

#class UserViewSet(viewsets.ReadOnlyModelViewSet):
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    


#class UserDetailViewSet(viewsets.ReadOnlyModelViewSet):
class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = UserDetail.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)    


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)