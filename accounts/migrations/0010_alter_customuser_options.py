# Generated by Django 5.1.5 on 2025-03-15 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('can_add_user', 'Can add user'), ('can_update_user', 'Can update user'), ('can_delete_user', 'Can delete user'))},
        ),
    ]
