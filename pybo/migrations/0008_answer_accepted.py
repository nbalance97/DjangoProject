# Generated by Django 2.2 on 2021-08-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0007_question_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
