from django.contrib import admin
from tests.models import Probationer

# Register your models here.
class ProbationerAdmin(admin.ModelAdmin):
	list_display = ('test', 'name', 'mark', 'precent', 'date')
	list_filter = ('test','date', 'mark')
	search_fields = ['name']

admin.site.register(Probationer, ProbationerAdmin)