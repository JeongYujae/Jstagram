# Generated by Django 4.0.4 on 2022-05-09 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jstagram', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='loation',
            new_name='location',
        ),
    ]
