# Generated by Django 5.0.3 on 2024-04-27 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spritlep', '0004_alter_customuser_fullname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
