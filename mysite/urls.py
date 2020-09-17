"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from article import views
from article import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^account/', include('account.urls', namespace='account', app_name='account')),
    url(r'^article/', include('article.urls', namespace='article', app_name='article')),
    url(r'^cif/', include('cif.urls', namespace='cif', app_name='cif')),
    url(r'^kernal/', include('kernal.urls', namespace='kernal', app_name='kernal')),
    url(r'^batch/', include('batch.urls', namespace='batch', app_name='batch')),
    url(r'^wechat/', include('wechat.urls', namespace='wechat', app_name='wechat')),
    url(r'^interface/', include('interface.urls', namespace='interface', app_name='interface')),
    url(r'^tst/', include('tst.urls', namespace='tst', app_name='tst')),
    #    url(r'^home/$', TemplateView.as_view(template_name="home.html")),

]