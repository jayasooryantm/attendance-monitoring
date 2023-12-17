# Generated by Django 4.2.7 on 2023-11-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0014_alter_employee_em_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("column1", models.CharField(max_length=255)),
                ("column2", models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name="employee",
            name="em_id",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]