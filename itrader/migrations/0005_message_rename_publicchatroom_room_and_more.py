# Generated by Django 4.0 on 2022-02-09 09:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itrader', '0004_alter_publicroomchatmessage_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('room', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('date_added',),
            },
        ),
        migrations.RenameModel(
            old_name='PublicChatRoom',
            new_name='Room',
        ),
        migrations.DeleteModel(
            name='PublicRoomChatMessage',
        ),
    ]
