from django.shortcuts import render
import datetime
from .forms import submitAnswer
from .models import TestCase, TestCaseTry, Team, Question, Setting
from checkyourself.settings import BASE_DIR

def submitTestCase(request):
    if request.method == 'POST':
        form = submitAnswer(request.POST)
        if form.is_valid():
            submitted_answer = form.cleaned_data['answer'].replace(' ','').split(',')
            question = form.cleaned_data['question']
            test_case = form.cleaned_data['test_case']
            test_case_obj = TestCase.objects.filter(question__number=question, number=test_case)
            if test_case_obj.exists():
                test_case_obj = test_case_obj.last()
                if test_case_obj.is_answered:
                    return render(request, 'submit.html', {
                        'message': 'You have already answered this test case',
                                                           'color': 'success'
                                    })
                if len(TestCaseTry.objects.filter(test_case=test_case_obj)) >= 3:

                    return render(request, 'submit.html', {
                        'message': 'You can attempt more than 3 times for each test case !',
                                                           'color': 'error'
                                    })
                is_correct = submitted_answer == test_case_obj.answer.split(' ')
                TestCaseTry.objects.create(test_case=test_case_obj, is_correct=is_correct, submitted_answer=submitted_answer)
                print(submitted_answer)
                print(type(submitted_answer))
                print(test_case_obj.answer.split(' '))
                print(type(test_case_obj.answer.split(' ')))
                if is_correct:
                    test_case_obj.is_answered = True
                    now = datetime.datetime.now()
                    timestamp = int(now.timestamp())
                    test_case_obj.answer_timestamp = timestamp
                    test_case_obj.save()
                    message = 'correct'
                    color = 'success'
                else:
                    message = 'wrong answer'
                    color = 'error'
                return render(request, 'submit.html', {'message': message, 'color': color})
            return render(request, 'submit.html', {'message': 'there is no such test case and question', 'color': 'error'})
        else:
            return render(request, 'submit.html', {'message': 'some kiri problem here'})
    else:

        return render(request, 'submit.html', {'message': '', 'color': ''})


def scorePage(request):
    result = {}
    teams = Team.objects.all()
    time_to_refresh = 1500
    setting = Setting.objects.all()
    if setting.exists():
        time_to_refresh = setting.last().reload_time
    for team in teams:
        result[f'{team.name}'] = {'score': 0, 'timestamp' : 0}

    test_case_objs = TestCase.objects.all()

    for test_case_obj in test_case_objs:
        if test_case_obj.is_answered:
            result[f'{test_case_obj.question.team.name}']['score'] += 30
        else:
            from_team = test_case_obj.question.from_team.name if test_case_obj.question.from_team else 3
            result[f'{from_team}']['score'] += 30

    return render(request, 'score.html', {'teams': result, 'time_to_refresh': time_to_refresh})

import json
def read_from_file(request):
    Team.objects.all().delete()
    TestCase.objects.all().delete()
    Question.objects.all().delete()

    print(BASE_DIR)
    # Opening JSON file
    f = open( f'{BASE_DIR}/web/end.json')
    second = open( f'{BASE_DIR}/web/second.json')
    seccond_data = json.load(second)



    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list

    for team in data:
        team_number = team['number']
        team_obj = Team.objects.create(name=team_number)
        team_obj.save()
        questions = team['questions']
        for question in questions:
            question_obj = Question.objects.create(number=question['number'], from_team=team_obj)
            question_obj.save()
            test_cases = question['testCases']
            for test_case in test_cases:
                test_case_answer = test_case['output']
                test_case_obj = TestCase.objects.create(number=test_case['number'],
                                                        question=question_obj
                                                        ,answer=test_case_answer)
                test_case_obj.save()


    for item in seccond_data:
        assigned_questions = item['assignedQuestions']
        team_number = item['GroupName']
        team_obj = Team.objects.get(name=team_number)
        for assQuestion in assigned_questions:
            print(int(assQuestion['QuestionName']))
            question_obj = Question.objects.get(number=int(assQuestion['QuestionName']))
            question_obj.team = team_obj
            question_obj.save()

    return render(request, 'submit.html', {'message': 'success'})
