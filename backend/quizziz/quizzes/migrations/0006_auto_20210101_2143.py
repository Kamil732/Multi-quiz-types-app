# Generated by Django 3.1.4 on 2021-01-01 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0005_auto_20210101_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(default='Welcome to my quiz!'),
        ),
    ]