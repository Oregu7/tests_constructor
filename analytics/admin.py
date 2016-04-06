from django.contrib import admin
from .models import Role, Specialization, Tested, Analytic

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

admin.site.register(Role)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Tested)
admin.site.register(Analytic)
