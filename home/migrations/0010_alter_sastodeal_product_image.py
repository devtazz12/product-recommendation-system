# Generated by Django 4.0.5 on 2023-01-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_sastodeal_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sastodeal_product',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
