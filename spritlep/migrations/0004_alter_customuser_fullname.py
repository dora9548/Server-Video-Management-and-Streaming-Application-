# Generated by Django 5.0.3 on 2024-04-26 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spritlep', '0003_customuser_fullname_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='FullName',
            field=models.CharField(max_length=100),
        ),
    ]
