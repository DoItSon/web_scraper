# Generated by Django 4.1.3 on 2022-12-06 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotdeal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='replay_count',
            new_name='reply_count',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='id',
        ),
        migrations.AlterField(
            model_name='deal',
            name='link',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
