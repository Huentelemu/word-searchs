# Generated by Django 3.0.8 on 2020-08-11 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzleprinter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordslist',
            name='encoding',
            field=models.TextField(choices=[('ISO-8859-1', 'ISO-8859-1'), ('utf-8', 'utf-8')], default='ISO-8859-1'),
        ),
    ]
