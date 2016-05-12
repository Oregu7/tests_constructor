from django.contrib import admin
from .models import Country

# Register your models here.
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_translate', 'image')
    search_fields = ['name']

#admin.site.register(Country, CountryAdmin)