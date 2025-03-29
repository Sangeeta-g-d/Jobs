# Generated by Django 5.0.6 on 2025-03-18 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_jobs', '0016_alter_appliedjob_job_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='area_of_interest',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='qualification',
            field=models.CharField(default='Latest education', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='skills',
            field=models.CharField(default='Enter your skills sets (separate by comma)', max_length=700),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='year_of_exp',
            field=models.CharField(default='Year of experience', max_length=250),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='year_of_passing',
            field=models.CharField(default='Year of passing', max_length=100),
        ),
    ]
