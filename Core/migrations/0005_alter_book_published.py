# Generated by Django 3.2.5 on 2021-07-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_auto_20210729_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.DateTimeField(),
        ),
    ]
