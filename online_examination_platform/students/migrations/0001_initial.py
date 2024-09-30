# Generated by Django 5.1.1 on 2024-09-29 21:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exam', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stu_Question',
            fields=[
                ('question_db_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='exam.question_db')),
                ('choice', models.CharField(default='E', max_length=3)),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'Student'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('exam.question_db',),
        ),
        migrations.CreateModel(
            name='StuExam_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examname', models.CharField(max_length=100)),
                ('score', models.IntegerField(default=0)),
                ('completed', models.IntegerField(default=0)),
                ('qpaper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.question_paper')),
                ('questions', models.ManyToManyField(to='students.stu_question')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'Student'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StuResults_DB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exams', models.ManyToManyField(to='students.stuexam_db')),
                ('student', models.ForeignKey(limit_choices_to={'groups__name': 'Student'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
