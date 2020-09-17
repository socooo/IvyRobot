from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^cifmas_add/$', views.cifmas_add, name="cifmas_add"),
    url(r'^cifmas_lst/$', views.cifmas_lst, name="cifmas_lst"),
    url(r'^cifmas_dsp/(?P<id>\d+)/$', views.cifmas_dsp, name="cifmas_dsp"),
    url(r'^cifmas_amd/(?P<id>\d+)/$', views.cifmas_amd, name="cifmas_amd"),
    url(r'^cifmas_amd_translate/(?P<id>\d+)/$', views.cifmas_amd_translate, name="cifmas_amd_translate"),
    url(r'^cifmas_del/$', views.cifmas_del, name="cifmas_del"),
    url(r'^cifmas_echart_0001/$', views.cifmas_echart_0001, name="cifmas_echart_0001"),
    url(r'^cifmas_echart_0002/$', views.cifmas_echart_0002, name="cifmas_echart_0002"),
    url(r'^cifmas_echart_0003/$', views.cifmas_echart_0003, name="cifmas_echart_0003"),
    url(r'^cifmas_tmp_add/$', views.cifmas_tmp_add, name="cifmas_tmp_add"),
    url(r'^cifmas_tmp_lst/$', views.cifmas_tmp_lst, name="cifmas_tmp_lst"),
    url(r'^cifmas_lst2lvl/$', views.cifmas_lst2lvl, name="cifmas_lst2lvl"),
    url(r'^cifmas_tmp_dsp/(?P<id>\d+)/$', views.cifmas_tmp_dsp, name="cifmas_tmp_dsp"),
    url(r'^cifmas_tmp_amd/(?P<id>\d+)/$', views.cifmas_tmp_amd, name="cifmas_tmp_amd"),
    url(r'^cifmas_tmp_amd2lvl/(?P<id>\d+)/$', views.cifmas_tmp_amd2lvl, name="cifmas_tmp_amd2lvl"),
    url(r'^cifmas_tmp_del/$', views.cifmas_tmp_del, name="cifmas_tmp_del"),
    url(r'^cifmas_tmp_del2lvl/$', views.cifmas_tmp_del2lvl, name="cifmas_tmp_del2lvl"),
    url(r'^cifmas_tmp_app/(?P<id>\d+)/$', views.cifmas_tmp_app, name="cifmas_tmp_app")
]