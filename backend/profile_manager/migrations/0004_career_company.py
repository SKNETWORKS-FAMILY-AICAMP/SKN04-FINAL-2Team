# Generated by Django 5.1.3 on 2025-01-09 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "profile_manager",
            "0003_alter_career_company_name_alter_company_company_name",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="career",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="careers",
                to="profile_manager.company",
            ),
        ),
    ]
