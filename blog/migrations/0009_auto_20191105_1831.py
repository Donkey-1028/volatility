# Generated by Django 2.1 on 2019-11-05 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20191105_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hitcount',
            name='ip',
            field=models.GenericIPAddressField(protocol='IPv4'),
        ),
    ]