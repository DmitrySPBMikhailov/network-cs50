# Generated by Django 5.0.1 on 2024-02-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("network", "0004_remove_post_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(null=True, verbose_name="Post"),
        ),
    ]
