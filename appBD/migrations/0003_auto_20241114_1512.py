# Generated by Django 3.1 on 2024-11-14 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBD', '0002_auto_20241114_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosusuario',
            name='rut',
            field=models.IntegerField(default=12345678, unique=True),
        ),
    ]