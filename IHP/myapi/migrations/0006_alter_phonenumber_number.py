# Generated by Django 4.0.1 on 2024-06-07 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0005_name_phonenumber_delete_globaldataset_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
