from django.contrib import admin
from tests.models import Probationer, ProbationerAnswer

# Register your models here.
class ProbationerAdmin(admin.ModelAdmin):
    list_display = ('option', 'get_full_name', 'get_group', 'mark', 'precent', 'date')
    list_filter = ('date', 'mark', 'user__study_group__specialization', 'user__study_group__course', 'user__study_group',)

    def get_full_name(self, obj):
        return obj.user.last_name + " " + obj.user.first_name

    def get_group(self, obj):
        return obj.user.study_group.name

    get_full_name.short_description = "Тестируемый"
    get_group.short_description = "Группа"
    get_group.admin_order_field = "user__study_group__name"
    get_full_name.admin_order_field = "user__last_name"

class ProbationerAnswerAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_group', 'get_answer_text', 'get_correct_answer')
    list_filter = ('answer__correct', )

    def get_full_name(self, obj):
        return obj.probationer.user.last_name + " " + obj.probationer.user.first_name

    def get_group(self, obj):
        return obj.probationer.user.study_group.name

    def get_answer_text(selfs, obj):
        return obj.answer.text

    def get_correct_answer(self, obj):
        return obj.answer.correct

    get_full_name.short_description = "Тестируемый"
    get_group.short_description = "Группа"
    get_answer_text.short_description = "Ответ"
    get_correct_answer.short_description = "Правильность"
    get_group.admin_order_field = "probationer__user__study_group__name"
    get_full_name.admin_order_field = "probationer__user__last_name"
    get_answer_text.admin_order_field = "answer__text"
    get_correct_answer.admin_order_field = "answer__correct"

admin.site.register(Probationer, ProbationerAdmin)
admin.site.register(ProbationerAnswer, ProbationerAnswerAdmin)