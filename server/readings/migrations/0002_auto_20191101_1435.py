# Generated by Django 2.0.7 on 2019-11-01 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='reading',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
