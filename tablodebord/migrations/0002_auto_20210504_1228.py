# Generated by Django 3.1.4 on 2021-05-04 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablodebord', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auteur',
            name='prenom',
        ),
        migrations.AlterField(
            model_name='livre',
            name='format',
            field=models.CharField(max_length=5),
        ),
    ]
