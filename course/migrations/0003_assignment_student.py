# Generated by Django 5.1.5 on 2025-02-06 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_assignment_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.student'),
        ),
    ]
