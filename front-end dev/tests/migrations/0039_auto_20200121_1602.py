# Generated by Django 2.2.6 on 2020-01-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0038_auto_20191210_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynmcqinfo',
            name='print_test',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='dyntestinfo',
            name='print_test',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
