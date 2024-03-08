from django.db import models

# Create your models here.





class Team(models.Model):
    name = models.CharField(max_length=1024)
    score = models.IntegerField(default=0, blank=True, null=True)
    sum_timestamp = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    number = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='doer_team') #
    from_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='from_team')
    def __str__(self):
        from_team_name = self.from_team.name if self.from_team else 'empty'
        to_team_name = self.team.name if self.team else 'empty'
        return f'Q{self.number} -> from_team : {from_team_name} | to_team_name : {to_team_name}'

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
