# Generated by Django 3.0 on 2020-02-15 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0013_auto_20200215_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penname',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
