from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from lessons import views
from .views import UserViewSet, UserDetailViewSet, LocationViewSet, ShopViewSet
from .views import EventViewSet, TagViewSet, PlanViewSet, TutorViewSet
from rest_framework.routers import DefaultRouter
from rest_framework import renderers
from .authentication import Login, Logout
from rest_framework.authtoken import views
from .views import CustomObtainAuthToken
#from .authentication import SocialSignUp

admin.autodiscover()
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'location', LocationViewSet)
router.register(r'users', UserViewSet)
router.register(r'user_detail', UserDetailViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'event', EventViewSet)
router.register(r'tag', TagViewSet)
router.register(r'plan', PlanViewSet)



# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
#    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
#    url(r'^sign_up/$', SignUp.as_view(), name="sign_up"),
#    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#	url(r'^', include('social.apps.django_app.urls', namespace='social')),
#    url(r'^login/$', auth_views.login),
#    url(r'^logout/$', auth_views.logout),
#    url(r'social/', include('social.apps.django_app.urls', namespace='social')),
#    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
#    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
#	url(r'^api/login/', include('rest_social_auth.urls_session')),
#	url(r'^api/login/', include('rest_social_auth.urls_token')),
#	url(r'^social_sign_up/$', views.SocialSignUp.as_view(), name="social_sign_up"),
#	url(r'^auth/', include('django.contrib.auth.urls', namespace='auth')),
	url(r'^authentication/$', Login.as_view()),
	url(r'^logout/$', Logout.as_view()),
#	url(r'^api-token-auth/', views.obtain_auth_token),
	url(r'^token_auth/', CustomObtainAuthToken.as_view()),
#	url(r'^social_sign_up/$', SocialSignUp.as_view(), name="social_sign_up"),
#	url(r'^', 'social.apps.django_app.urls', name="social"),
#	url(r'^user_detail/(?P<pk>\d+)/$', views.UserDetailRetrieve.as_view(), name="user_detail"),

]
