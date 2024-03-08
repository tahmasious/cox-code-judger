# Generated by Django 4.2.11 on 2024-03-08 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_team_score_team_sum_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='from_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_team', to='web.team'),
        ),
        migrations.AlterField(
            model_name='question',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doer_team', to='web.team'),
        ),
    ]