# app/admin.py
from django.contrib import admin
from .models import Liquor
from import_export.admin import ImportExportModelAdmin


class LiquorAdmin(ImportExportModelAdmin):
    exclude = ['bookmark']


admin.site.register(Liquor, LiquorAdmin)
