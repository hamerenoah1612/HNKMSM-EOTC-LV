# Generated by Django 4.2 on 2024-05-29 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventgallery_posteventimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventgallery',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventscategory'),
        ),
    ]
