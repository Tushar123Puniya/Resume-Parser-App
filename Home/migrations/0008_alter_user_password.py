# Generated by Django 3.2.25 on 2024-06-28 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_auto_20240628_0559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=10000),
        ),
    ]
