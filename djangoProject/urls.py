from django.conf.urls import include, url
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include('lessons.urls')),
]
