# Generated by Django 2.1 on 2019-11-03 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_title',
            new_name='post',
        ),
    ]
