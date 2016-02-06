from django.contrib import admin
from constructor.models import Test, Query, Answer, Category
# Register your models here.

class TestAdmin(admin.ModelAdmin):
	list_display = ('title', 'creator', 'date')
	search_fields = ['title']
	list_filter = ('date',)

admin.site.register(Test, TestAdmin)
admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(Category)