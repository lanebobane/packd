# Generated by Django 4.0 on 2024-08-01 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("packr", "0007_pack_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pack",
            name="bag",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bag",
                to="packr.item",
            ),
        ),
    ]
