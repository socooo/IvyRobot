from django.conf.urls import url
from . import views, list_views

from django.conf import settings

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^article-column/$', views.article_column, name="article_column"),
    url(r'^article-column/(?P<id>\d+)/$', views.column_detail, name="column_detail"),
    url(r'^rename-column/$', views.rename_article_column, name="rename_article_column"),
    url(r'^delete-column/$', views.del_article_column, name="del_article_column"),
    url(r'^article-post/$', views.article_post, name="article_post"),
    url(r'^article-translate/$', views.article_translate, name="article_translate"),
    url(r'^article-list/$', views.article_list, name="article_list"),
    url(r'^article-detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.article_detail, name="article_detail"),
    url(r'^article_pyechart1/$', views.article_pyechart1, name="article_pyechart1"),
    #url(r'^list-article-titles/$', list_views.article_titles, name="article_titles"),
    url(r'^list-article-titles/(?P<username>[-\w]+)/$', list_views.article_titles, name="article_titles"),
]

handler404 = "blog.views.page_not_found"
handler500 = "blog.views.page_error"
