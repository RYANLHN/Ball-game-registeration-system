# Generated by Django 3.1.3 on 2020-11-29 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainIndex', '0005_auto_20201129_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerlist',
            name='contactNumber',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='playerlist',
            name='player1Id',
            field=models.CharField(max_length=19),
        ),
        migrations.AlterField(
            model_name='playerlist',
            name='player2Id',
            field=models.CharField(max_length=19, null=True),
        ),
        migrations.AlterField(
            model_name='playerlist',
            name='player2Name',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
