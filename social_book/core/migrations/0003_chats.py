# Generated by Django 4.2.4 on 2023-09-24 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.TextField()),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_as_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats_as_user2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
