from django.contrib import admin

from .models import *

class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['number', 'question', 'answer', 'is_answered', 'answer_timestamp', 'get_test_case_question',
                      'get_test_case_from_team', 'get_test_case_team',

                    ]
    list_filter = ('number', 'question', 'is_answered', 'answer_timestamp','question__number', 'question__team', 'question__from_team' )

    def get_test_case_question(self, obj):
        if obj.question :
            return obj.question.number
        return ''

    def get_test_case_from_team(self,obj):
        return obj.question.from_team

    def get_test_case_team(self,obj):
        return obj.question.team

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['number', 'team', 'from_team']
    list_filter = ['number', 'team', 'from_team']




class TestCaseTriesAdmin(admin.ModelAdmin):
    list_filter = [ 'is_correct', 'submitted_answer', 'test_case__number',
                    'test_case__question__number', 'test_case__question__team', 'test_case__question__from_team']
    list_display =  ( 'is_correct', 'submitted_answer',
                      'get_test_case_number', 'get_test_case_question',
                      'get_test_case_from_team', 'get_test_case_team')

    def get_test_case_number(self, obj):
        return obj.test_case.number

    def get_test_case_question(self, obj):
        if obj.test_case.question :
            return obj.test_case.question.number
        return ''

    def get_test_case_from_team(self,obj):
        return obj.test_case.question.from_team

    def get_test_case_team(self,obj):
        return obj.test_case.question.team
# Register your models here.
admin.site.register(Team)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestCaseTry, TestCaseTriesAdmin)
admin.site.register(Setting)
