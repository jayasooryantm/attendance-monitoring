# Generated by Django 4.2.6 on 2023-11-26 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0009_alter_record_remark"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="em_id",
            field=models.CharField(max_length=20),
        ),
    ]
