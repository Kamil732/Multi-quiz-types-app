# Generated by Django 3.1.4 on 2021-01-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='solved_quizzes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
