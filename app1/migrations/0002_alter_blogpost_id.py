# Generated by Django 5.0.1 on 2024-01-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
