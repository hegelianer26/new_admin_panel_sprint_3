# Generated by Django 3.2 on 2023-06-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0017_remove_personfilmwork_person_film_film_wo_6b9cac_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work_id', 'person_id', 'role'], name='person_film_film_wo_6b9cac_idx'),
        ),
    ]
