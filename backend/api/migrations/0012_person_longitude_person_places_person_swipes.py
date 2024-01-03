# Generated by Django 5.0 on 2024-01-02 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_person_latitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='places',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='swipes',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
