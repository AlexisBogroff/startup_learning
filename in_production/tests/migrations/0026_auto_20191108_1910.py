# Generated by Django 2.2.5 on 2019-11-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0025_auto_20191108_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pass_dyntest',
            name='activated',
        ),
        migrations.AddField(
            model_name='dyntest',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]
