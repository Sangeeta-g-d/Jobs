# Generated by Django 5.0.6 on 2025-02-15 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_jobs', '0011_alter_appliedjob_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliedjob',
            name='job_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
