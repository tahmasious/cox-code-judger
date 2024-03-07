from django.shortcuts import render
import datetime
from .forms import submitAnswer
from .models import TestCase, TestCaseTry, Team, Question, Setting


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
                is_correct = submitted_answer == test_case_obj.answer.split(',')
                TestCaseTry.objects.create(test_case=test_case_obj, is_correct=is_correct, submitted_answer=submitted_answer)
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
            return render(request, 'submit.html', {'message': 'there is no such test case and question'})
        else:
            return render(request, 'submit.html', {'message': 'some kiri problem here'})
    else:

        return render(request, 'submit.html', {'message': '', 'color': ''})


def scorePage(request):
    result = []
    teams = Team.objects.all()
    time_to_refresh = 1500
    setting = Setting.objects.all()
    if setting.exists():
        time_to_refresh = setting.last().reload_time
    for team in teams:
        team_score = 0
        team_timestamps = 0
        team_questions = Question.objects.filter(team=team)
        test_cases = TestCase.objects.filter(question__in=team_questions)
        for test_case in test_cases:
            team_score += 10 if test_case.is_answered else 0
            team_timestamps += test_case.answer_timestamp if test_case.answer_timestamp else 0
        result.append({
            'name': team.name,
            'score': team_score,
            'timestamps': team_timestamps
        })

    return render(request, 'score.html', {'teams': sorted(result, key=lambda x: x['score'])[::-1], 'time_to_refresh': time_to_refresh})
