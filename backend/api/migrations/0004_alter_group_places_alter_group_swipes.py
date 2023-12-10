# Generated by Django 4.2 on 2023-12-09 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_group_places_group_swipes_alter_person_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='places',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='swipes',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
