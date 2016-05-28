from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Specialization, Group, User
from .forms import AdminUserAddForm, AdminUserChangeForm


# Register your models here.
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')

class GroupAdmin(admin.ModelAdmin):
    list_filter = ('specialization', 'course')
    list_display = ('name', 'specialization', 'course')
    search_fields = ('name',)

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    raw_id_fields = ('study_group', )
    filter_horizontal = ('subjects', 'groups')
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'study_group', 'subjects')}
        ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'study_group',
            'subjects'
        )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Group, GroupAdmin)