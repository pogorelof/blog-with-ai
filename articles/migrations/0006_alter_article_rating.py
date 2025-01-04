# Generated by Django 5.1.3 on 2024-12-04 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
