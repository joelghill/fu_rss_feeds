# Generated by Django 3.0 on 2020-02-15 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0011_auto_20200215_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedentry',
            name='license',
            field=models.URLField(blank=True, null=True),
        ),
    ]
