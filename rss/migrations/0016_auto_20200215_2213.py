# Generated by Django 3.0 on 2020-02-15 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0015_auto_20200215_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycontent',
            name='base',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrycontent',
            name='language',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrycontent',
            name='type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrycontent',
            name='value',
            field=models.TextField(blank=True, null=True),
        ),
    ]
