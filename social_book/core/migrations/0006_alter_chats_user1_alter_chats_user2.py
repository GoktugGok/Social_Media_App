# Generated by Django 4.2.4 on 2023-09-24 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_chats_user1_alter_chats_user2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chats',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]
