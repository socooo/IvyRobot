from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cifmas_lst_inq/$', views.cifmas_lst_inq, name="cifmas_lst_inq"),
]
