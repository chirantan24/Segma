# Generated by Django 3.1.7 on 2021-05-22 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segmapp', '0002_auto_20210518_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='bio',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
