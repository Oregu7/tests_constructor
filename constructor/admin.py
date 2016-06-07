from django.contrib import admin
from constructor.models import Test, Query, Answer, Category, Option
from suit.admin import SortableTabularInline
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

class QueryAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'point')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('query', 'text', 'correct')
    search_fields = ['text']
    list_filter = ('correct', )

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'url']
    list_display = ('name', 'url')

admin.site.register(Test, TestAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Option, OptionAdmin)