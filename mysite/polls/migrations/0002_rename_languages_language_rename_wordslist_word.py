# Generated by Django 5.0.4 on 2024-05-04 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Languages',
            new_name='Language',
        ),
        migrations.RenameModel(
            old_name='WordsList',
            new_name='Word',
        ),
    ]
