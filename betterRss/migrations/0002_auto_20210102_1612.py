# Generated by Django 3.1.3 on 2021-01-02 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('betterRss', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rssitem',
            name='nlp_summary',
        ),
        migrations.RemoveField(
            model_name='rssitem',
            name='rss_feed',
        ),
        migrations.RemoveField(
            model_name='rssitem',
            name='save_date',
        ),
        migrations.DeleteModel(
            name='RssFeed',
        ),
    ]