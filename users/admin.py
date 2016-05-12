from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Specialization, Subject, Group, User
from .forms import AdminUserAddForm, AdminUserChangeForm


# Register your models here.
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    filter_horizontal = ('subjects', 'groups')
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'study_group', 'groups', 'subjects')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'study_group',
            'groups',
            'subjects'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Subject)
admin.site.register(Group)