# Generated by Django 3.1.7 on 2022-01-28 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablodebord', '0003_livre_resume'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='reference',
            field=models.CharField(default='REFERENCE', max_length=20),
        ),
    ]