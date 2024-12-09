# Generated by Django 5.1.1 on 2024-12-04 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_user_last_login'),
        ('mycoinApp', '0011_passwordresettoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetNameCoins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_name', models.CharField(blank=True, max_length=64, null=True)),
                ('coin_list', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='coinstatecondition',
            name='inclusion_status',
            field=models.CharField(choices=[('Y', 'Compulsory'), ('R', 'Recommended'), ('N', 'Not Included')], default='N', max_length=1),
        ),
        migrations.CreateModel(
            name='UserSetOfCoin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_counts', models.JSONField(blank=True, null=True)),
                ('set_name', models.CharField(blank=True, max_length=64, null=True)),
                ('coin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mycoinApp.coin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
            ],
            options={
                'unique_together': {('user', 'coin')},
            },
        ),
        migrations.CreateModel(
            name='UniverseCoinSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.user')),
                ('coin_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycoinApp.usersetofcoin')),
            ],
        ),
    ]
