# Generated by Django 3.2.25 on 2024-06-28 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cv_limit',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='user',
            name='trials',
            field=models.IntegerField(default=10),
        ),
    ]