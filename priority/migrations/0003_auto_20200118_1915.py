# Generated by Django 2.2.7 on 2020-01-18 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('priority', '0002_clients_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clients',
            name='job_title',
        ),
        migrations.AlterField(
            model_name='clients',
            name='priority_status',
            field=models.CharField(choices=[('high', 'high'), ('mid', 'mid'), ('low', 'low'), ('none', 'none')], default='none', max_length=5),
        ),
        migrations.AlterField(
            model_name='clients',
            name='supervisor',
            field=models.CharField(max_length=20, verbose_name='Pincipal Investigator'),
        ),
    ]
