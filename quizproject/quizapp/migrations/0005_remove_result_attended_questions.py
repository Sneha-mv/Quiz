# Generated by Django 4.2.16 on 2024-11-25 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_result_attended_questions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='attended_questions',
        ),
    ]