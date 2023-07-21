# Generated by Django 4.2.3 on 2023-07-21 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meets", "0004_remove_record_bodyweight_kg_alter_result_division"),
    ]

    operations = [
        migrations.RenameField(
            model_name="result",
            old_name="bench1_kg",
            new_name="bench1",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="bench2_kg",
            new_name="bench2",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="bench3_kg",
            new_name="bench3",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="deadlift1_kg",
            new_name="bodyweight",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="deadlift2_kg",
            new_name="deadlift1",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="deadlift3_kg",
            new_name="deadlift2",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="squat1_kg",
            new_name="deadlift3",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="squat2_kg",
            new_name="squat1",
        ),
        migrations.RenameField(
            model_name="result",
            old_name="squat3_kg",
            new_name="squat2",
        ),
        migrations.RemoveField(
            model_name="result",
            name="bodyweight_kg",
        ),
        migrations.RemoveField(
            model_name="result",
            name="total_kg",
        ),
        migrations.RemoveField(
            model_name="result",
            name="weight_class_kg",
        ),
        migrations.AddField(
            model_name="result",
            name="age_group",
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="date_of_birth",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="discipline",
            field=models.CharField(
                choices=[
                    ("S", "Squat"),
                    ("B", "Bench press"),
                    ("D", "Deadlift"),
                    ("T", "Total"),
                    ("BP", "Bench press single lift"),
                ],
                max_length=2,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="equipment",
            field=models.CharField(
                choices=[("E", "equipped"), ("R", "raw")], max_length=1, null=True
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="lot",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="sex",
            field=models.CharField(
                choices=[("M", "male"), ("F", "female")], max_length=1, null=True
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="squat3",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="state",
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="team",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="total",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="weight_class",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="result",
            name="drug_tested",
            field=models.CharField(max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name="result",
            name="placing",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="result",
            name="points",
            field=models.FloatField(null=True),
        ),
    ]