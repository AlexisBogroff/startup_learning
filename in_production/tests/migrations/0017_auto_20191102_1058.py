# Generated by Django 2.2.5 on 2019-11-02 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_auto_20191102_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pass_dyntest',
            name='q_num',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
