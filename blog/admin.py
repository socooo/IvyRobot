# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BlogArticles
from django.contrib.admin.templatetags.admin_list import date_hierarchy

class BlogArticlesAdmin(admin.ModelAdmin):
    list_display=("title","author","publish")
    list_filter=("publish","author")
    search_field=('title',"body")
    raw_id_fields=("author",)
    date_hierarchy="publish"
    ordering=['publish','author']
    
admin.site.register(BlogArticles,BlogArticlesAdmin)