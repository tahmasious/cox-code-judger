from django.db import models

# Create your models here.





class Team(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name

class Question(models.Model):
    number = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Q{self.number} -> team : {self.team.name}'

class TestCase(models.Model):
    number = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.CharField(max_length=1024)
    is_answered = models.BooleanField(default=False, null=True, blank=True)
    answer_timestamp = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'T{self.number} -> question : {self.question.number}'


class TestCaseTry(models.Model):
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    submitted_answer = models.CharField(max_length=256)

    def __str__(self):
        return f'try for {self.test_case}'


class Setting(models.Model):
    reload_time = models.IntegerField()
