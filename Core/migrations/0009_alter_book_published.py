# Generated by Django 3.2.5 on 2021-07-31 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0008_alter_book_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.DateField(),
        ),
    ]
