from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from lessons import views
from .views import LessonViewSet, UserViewSet, UserDetailViewSet, SignUp
from .views import SchoolViewSet, SchoolOwnerViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import renderers

admin.autodiscover()
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'lessons', LessonViewSet)
router.register(r'users', UserViewSet)
router.register(r'user_detail', UserDetailViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'school_owners', SchoolOwnerViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^sign_up/$', SignUp.as_view(), name="sign_up"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', auth_views.logout),
]

"""
lesson_list = LessonViewSet.as_view({
	'get':'list'
	'post':'create'
	})
lesson_detail = LessonViewSet.as_view({
	'get':'retrieve'
	'put':'update'
	'patch':'partial_update'
	'delete':'destroy'
	})
user_list = UserViewSet.as_view({
	'get':'list'
	})
user_detail = UserViewSet.as_view({
	'get':'retrieve'
	})

#API endpoints
urlpatterns = format_suffix_patterns([
	url(r'^$',views.api_root),
    url(r'^lessons/$', lesson_list,name='lesson-list'),
    url(r'^lessons/(?P<pk>[0-9]+)/$',lesson_detail,name='lesson-detail'),
    url(r'^users/$', user_list,name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', user_detail,name='user-detail'),
    ])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
"""