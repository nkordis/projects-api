# Generated by Django 3.2.25 on 2024-05-13 18:05

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20240507_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(null=True, upload_to=core.models.project_image_file_path),
        ),
    ]
