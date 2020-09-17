from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tst_https_upload/$', views.tst_https_upload, name="tst_https_upload"),
    url(r'^tst_smtp_send/$', views.tst_smtp_send, name="tst_smtp_send"),
    url(r'^tst_redis/$', views.tst_redis, name="tst_redis"),
    url(r'^tst_url/$', views.tst_url, name="tst_url"),
]