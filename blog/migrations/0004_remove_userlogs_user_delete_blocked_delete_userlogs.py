# Generated by Django 4.1.4 on 2022-12-25 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userlogs',
            name='user',
        ),
        migrations.DeleteModel(
            name='Blocked',
        ),
        migrations.DeleteModel(
            name='UserLogs',
        ),
    ]