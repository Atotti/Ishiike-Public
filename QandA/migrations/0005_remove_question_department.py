# Generated by Django 4.2 on 2023-09-30 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QandA', '0004_rename_faculty_and_department_question_faculty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='department',
        ),
    ]
