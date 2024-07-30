# Generated by Django 5.0.7 on 2024-07-26 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_ingredient_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='code',
            field=models.CharField(default='0', max_length=50, verbose_name='식품코드'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='item',
            field=models.CharField(default='NONE', max_length=50, verbose_name='품목'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(default='NONE', max_length=50, verbose_name='품종'),
        ),
    ]