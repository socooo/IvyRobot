from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^check_signature/$', views.check_signature, name="check_signature"),
    url(r'^create_menu/$', views.create_menu, name="create_menu"),
]
