# Generated by Django 3.2.25 on 2024-06-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_id',
            field=models.TextField(),
        ),
    ]
