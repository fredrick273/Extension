# Generated by Django 4.1.7 on 2024-03-13 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_codes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codes',
            name='code',
        ),
    ]
