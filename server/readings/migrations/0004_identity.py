# Generated by Django 2.0.7 on 2019-11-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readings', '0003_auto_20191101_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Identity', models.IntegerField(default=0)),
            ],
        ),
    ]
