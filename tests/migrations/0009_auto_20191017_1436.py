# Generated by Django 2.2.5 on 2019-10-17 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_pass_mcqtest_end_session_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pass_mcqtest_end_session',
            old_name='note',
            new_name='mark',
        ),
    ]
