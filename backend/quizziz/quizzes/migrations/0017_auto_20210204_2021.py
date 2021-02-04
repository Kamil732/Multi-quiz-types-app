# Generated by Django 3.1.5 on 2021-02-04 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('quizzes', '0016_auto_20210204_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgeanswer',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='preferentialanswer',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='psychologyanswer',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='question',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='universalanswer',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='knowledgeanswer',
            name='answer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='preferentialanswer',
            name='answer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='psychologyanswer',
            name='answer',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='universalanswer',
            name='answer',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]