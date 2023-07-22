# Generated by Django 4.2.3 on 2023-07-21 11:21

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumApp', '0004_reddemcommunity_image_alter_reddemcommunity_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=False, editable=False, populate_from='title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reddemcommunity',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=False, editable=False, populate_from='title'),
            preserve_default=False,
        ),
    ]