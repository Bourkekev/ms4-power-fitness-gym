# Generated by Django 3.1.3 on 2020-12-15 20:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='newspost',
            name='status',
            field=models.IntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=0),
        ),
    ]
