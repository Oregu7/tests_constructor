from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Specialization, Group, User
from .serializers import GroupSerializer
from .forms import AdminUserAddForm, AdminUserChangeForm
from django_excel import make_response_from_records
import pyexcel.ext.xlsx

# Register your models here.
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ['name']

class GroupAdmin(admin.ModelAdmin):
    list_filter = ('specialization', 'course')
    list_display = ('name', 'specialization', 'course', 'secret_key')
    search_fields = ('name',)

    actions = ['set_secret_keys', 'send_files']

    def send_files(self, request, queryset):
        response = []
        groups = GroupSerializer(queryset, many=True).data
        for group in groups:
            response.append({
                'Название': group['name'],
                'Специализация': group['specialization']['name'],
                'Курс': group['course'],
                'Секретный код': group['secret_key']
            })
        return make_response_from_records(response, file_type='xlsx', file_name="groups")

    def set_secret_keys(self, request, queryset):
        for group in queryset:
            group.secret_key = Group.generate_secret_code()
            group.save()

    send_files.short_description = "Скачать данные в формате *.xlsx"
    set_secret_keys.short_description = "Изменить секретный код"

class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserAddForm
    list_filter = ('study_group__course', 'study_group__specialization', 'study_group', 'is_staff')
    list_display = ('last_name', 'first_name', 'study_group', 'get_specialization', 'get_course', 'is_staff', 'is_superuser')
    search_fields = ['last_name']
    raw_id_fields = ('study_group', )
    filter_horizontal = ('subjects', 'groups')
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'study_group', 'subjects')}
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

    def get_specialization(self, obj):
        group = obj.study_group
        if group is not None:
            return group.specialization.name
        else:
            return "-"

    def get_course(self, obj):
        group = obj.study_group
        if group is not None:
            return group.course
        else:
            return "-"

    get_specialization.short_description = "Специализация"
    get_course.short_description = "Курс"
    get_specialization.admin_order_field = "study_group__specialization__name"
    get_course.admin_order_field = "study_group__course"

admin.site.register(User, UserAdmin)
admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Group, GroupAdmin)