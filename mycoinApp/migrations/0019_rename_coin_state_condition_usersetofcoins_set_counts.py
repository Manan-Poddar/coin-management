# Generated by Django 5.1.1 on 2024-11-30 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycoinApp', '0018_remove_usersetofcoins_coin_set_usersetofcoins_coin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersetofcoins',
            old_name='coin_state_condition',
            new_name='set_counts',
        ),
    ]