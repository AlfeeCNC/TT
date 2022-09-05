# Generated by Django 4.1 on 2022-09-04 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0001_initial'),
        ('MemberSystem', '0003_action_tx_hash_alter_action_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_plan', to='Club.plan'),
        ),
        migrations.AlterField(
            model_name='action',
            name='tx_hash',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]