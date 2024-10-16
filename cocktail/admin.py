# app/admin.py
from django.contrib import admin
from .models import Cocktail
from import_export.admin import ImportExportModelAdmin


class CocktailAdmin(ImportExportModelAdmin):
    exclude = ['bookmark']


admin.site.register(Cocktail, CocktailAdmin)
