# Generated by Django 3.2 on 2022-11-24 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20221124_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='createddddd'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='createddddd'),
        ),
        migrations.AlterField(
            model_name='person',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='createddddd'),
        ),
    ]
