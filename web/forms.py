from django import forms

class submitAnswer(forms.Form):
    answer = forms.CharField(max_length=264)
    question = forms.IntegerField()
    test_case = forms.IntegerField()
