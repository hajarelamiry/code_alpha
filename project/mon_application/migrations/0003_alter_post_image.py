# Generated by Django 5.0.4 on 2024-09-22 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mon_application', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='avatar-3814049_1280.png', upload_to='post_images'),
        ),
    ]
