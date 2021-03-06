# Generated by Django 3.1.6 on 2021-02-24 18:39

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0037_remove_psychologyresults_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='psychologyresults',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='xd', editable=False, max_length=120, populate_from='result', unique_with=['quiz']),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizpunctation',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='xd', editable=False, max_length=120, populate_from='result', unique_with=['quiz']),
            preserve_default=False,
        ),
    ]
