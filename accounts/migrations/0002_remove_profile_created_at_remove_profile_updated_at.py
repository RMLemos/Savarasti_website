# Generated by Django 4.2 on 2024-03-17 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='updated_at',
        ),
    ]
