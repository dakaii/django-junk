from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from lessons import views
from .views import LessonViewSet, UserViewSet, UserDetailViewSet, BookingViewSet
from .views import SchoolViewSet, SchoolOwnerViewSet
#from .views import SocialSignUp
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from .authentication import Login, Logout

admin.autodiscover()
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'lessons', LessonViewSet)
router.register(r'users', UserViewSet)
router.register(r'user_detail', UserDetailViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'school_owners', SchoolOwnerViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'login', Login)
router.register(r'logout', Logout)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
#    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#    url(r'^sign_up/$', SignUp.as_view(), name="sign_up"),
#    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#	url(r'social', include('social.apps.django_app.urls', namespace='social')),
#    url(r'^login/$', auth_views.login),
#    url(r'^logout/$', auth_views.logout),
#    url('', include('social.apps.django_app.urls', namespace='social')),
#    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
#	url(r'^api/login/', include('rest_social_auth.urls_session')),
#	url(r'^api/login/', include('rest_social_auth.urls_token')),
#	url(r'^social_sign_up/$', views.SocialSignUp.as_view(), name="social_sign_up"),
#	url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
]
