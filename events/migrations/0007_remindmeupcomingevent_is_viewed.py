# Generated by Django 4.2 on 2025-05-23 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_remindmeupcomingevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='remindmeupcomingevent',
            name='is_viewed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
