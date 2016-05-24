from django.contrib import admin
from tests.models import Probationer, ProbationerAnswer

# Register your models here.
class ProbationerAdmin(admin.ModelAdmin):
    list_display = ('option', 'user', 'mark', 'precent', 'date')
    list_filter = ('date', 'mark')

admin.site.register(Probationer, ProbationerAdmin)
admin.site.register(ProbationerAnswer)