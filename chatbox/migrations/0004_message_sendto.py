# Generated by Django 4.0.3 on 2022-05-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0003_delete_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='sendto',
            field=models.TextField(default='Anonymous', max_length=100),
        ),
    ]