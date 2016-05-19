from django.contrib import admin
from constructor.models import Test, Query, Answer, Category, Option
# Register your models here.

class TestAdmin(admin.ModelAdmin):
    filter_horizontal = ('group_access', )
    list_display = ('title', 'creator', 'date')
    search_fields = ['title']
    list_filter = ('date',)

class OptionAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions',)
    list_display = ('test', 'number', 'public_access')
    list_filter = ('public_access', )

admin.site.register(Test, TestAdmin)
admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Option, OptionAdmin)