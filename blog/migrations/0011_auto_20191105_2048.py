# Generated by Django 2.1 on 2019-11-05 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20191105_2039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hitcount',
            name='post',
        ),
        migrations.AddField(
            model_name='hitcount',
            name='post',
            field=models.ForeignKey(default=1234, on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
            preserve_default=False,
        ),
    ]
