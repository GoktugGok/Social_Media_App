# Generated by Django 4.2.4 on 2023-09-30 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_likepost_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likepost',
            options={'ordering': ['created_at']},
        ),
    ]