# Generated by Django 4.2 on 2023-10-09 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("llmevaluator", "0007_chatbotmessagearray_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="batchllmjob",
            name="include_gpt_35",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="batchllmjob",
            name="include_gpt_4",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="batchllmjob",
            name="run_n_times",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="batchllmjob",
            name="temperature_range",
            field=models.BooleanField(default=False),
        ),
    ]
