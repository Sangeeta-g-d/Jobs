# Generated by Django 5.0.6 on 2025-02-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_jobs', '0006_alter_jobs_job_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='category',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
