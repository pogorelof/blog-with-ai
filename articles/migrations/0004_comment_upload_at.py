# Generated by Django 5.1.3 on 2024-12-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_article_options_alter_article_rating_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upload_at',
            field=models.DateTimeField(auto_now_add=True, default='1999-01-01 10:00'),
            preserve_default=False,
        ),
    ]
