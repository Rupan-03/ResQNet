# Generated by Django 4.2.3 on 2024-01-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rescuenetApp', '0003_alter_customuser_area_of_expertise'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(max_length=255, null=True),
        ),
    ]