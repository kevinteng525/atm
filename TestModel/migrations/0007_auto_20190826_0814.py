# Generated by Django 2.2.3 on 2019-08-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestModel', '0006_auto_20190826_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testplan',
            name='desc',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Description'),
        ),
    ]
