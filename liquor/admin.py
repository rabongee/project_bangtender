# app/admin.py
from django.contrib import admin
from .models import Liquor
from import_export.admin import ImportExportModelAdmin


class LiquorAdmin(ImportExportModelAdmin):
    """관리자 페이지 Liquor ImportExport
    """

    exclude = ['bookmark']


admin.site.register(Liquor, LiquorAdmin)
