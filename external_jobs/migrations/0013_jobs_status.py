# Generated by Django 5.0.6 on 2025-02-16 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_jobs', '0012_appliedjob_job_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='status',
            field=models.CharField(default='Active', max_length=400),
        ),
    ]
