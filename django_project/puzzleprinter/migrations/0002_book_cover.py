# Generated by Django 3.0.4 on 2020-05-19 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzleprinter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='books/covers/'),
        ),
    ]
