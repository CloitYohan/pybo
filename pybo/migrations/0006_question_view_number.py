# Generated by Django 4.0.3 on 2024-01-04 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0005_answer_voter_question_voter_alter_answer_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='view_number',
            field=models.IntegerField(default='0'),
        ),
    ]
