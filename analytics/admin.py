from django.contrib import admin
from .models import Role, Tested, Analytic
class TestedAdmin(admin.ModelAdmin):
    list_filter = ('date', 'role', 'course', 'specialization')

admin.site.register(Role)
admin.site.register(Tested, TestedAdmin)
admin.site.register(Analytic)
