from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from lessons import views

urlpatterns = [
    url(r'^lessons/$',views.LessonList.as_view()),
    url(r'^lessons/(?P<pk>[0-9]+)/$',views.LessonDetail.as_view()),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)