# Generated by Django 5.1.5 on 2025-02-06 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='student',
        ),
    ]
