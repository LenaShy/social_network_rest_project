# Generated by Django 2.1.2 on 2018-10-05 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20181005_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='draft',
        ),
    ]
