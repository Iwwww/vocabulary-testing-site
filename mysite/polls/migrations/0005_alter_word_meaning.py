# Generated by Django 5.0.4 on 2024-05-05 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_word_meaning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='meaning',
            field=models.CharField(max_length=300),
        ),
    ]
