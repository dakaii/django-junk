from .models import Lesson
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .serializers import LessonSerializer
from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, renderers, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'lessons': reverse('lesson-list', request=request, format=format)
    })

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#class LessonList(generics.ListCreateAPIView):
#    queryset = Lesson.objects.all()
#    serializer_class = LessonSerializer
#    permission_classes = (IsAuthenticatedOrReadOnly,)
#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)


#class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Lesson.objects.all()
#    serializer_class = LessonSerializer
#    permission_classes = (IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

#class UserList(generics.ListAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

#class UserDetail(generics.RetrieveAPIView):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
