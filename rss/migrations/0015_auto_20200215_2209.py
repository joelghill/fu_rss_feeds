# Generated by Django 3.0 on 2020-02-15 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0014_auto_20200215_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycontent',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='rss.FeedEntry'),
        ),
    ]
