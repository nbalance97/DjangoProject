# Generated by Django 2.2 on 2021-09-10 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0008_answer_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
