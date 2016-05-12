from django.contrib import admin
from tests.models import Probationer, ProbationerAnswers

# Register your models here.
class ProbationerAdmin(admin.ModelAdmin):
    list_display = ('test', 'mark', 'precent', 'date')
    list_filter = ('test', 'date', 'mark')

admin.site.register(Probationer, ProbationerAdmin)
admin.site.register(ProbationerAnswers)