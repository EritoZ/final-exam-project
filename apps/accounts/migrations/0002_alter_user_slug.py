# Generated by Django 4.2.3 on 2023-07-21 12:11

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=False, editable=False, populate_from='username'),
            preserve_default=False,
        ),
    ]
