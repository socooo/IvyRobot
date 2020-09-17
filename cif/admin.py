# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cif_mas,Cif_mas_tmp
from django.contrib.admin.templatetags.admin_list import date_hierarchy


class Cif_masAdmin(admin.ModelAdmin):
    list_display = ("id_type", "id_country", "id_no")
    list_filter = ("id_country",)

class Cif_mas_tmpAdmin(admin.ModelAdmin):
    list_display = ("id_type", "id_country", "id_no")
    list_filter = ("id_country",)



admin.site.register(Cif_mas, Cif_masAdmin)
admin.site.register(Cif_mas_tmp, Cif_mas_tmpAdmin)