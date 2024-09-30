# app/admin.py
from django.contrib import admin
from .models import Cocktail
from import_export.admin import ImportExportModelAdmin


class CocktailAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Cocktail, CocktailAdmin)
