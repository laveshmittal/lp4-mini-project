# Generated by Django 3.0.4 on 2021-04-27 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20190929_1142'),
    ]

    operations = [
        migrations.DeleteModel(
            name='agegroup',
        ),
        migrations.DeleteModel(
            name='education',
        ),
        migrations.DeleteModel(
            name='escapes',
        ),
        migrations.DeleteModel(
            name='periodofsentence',
        ),
    ]
