# Generated by Django 5.0.4 on 2024-06-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfiles',
            name='file_name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='userfiles',
            name='file_url',
            field=models.URLField(blank=True),
        ),
    ]
