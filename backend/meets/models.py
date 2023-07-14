from django.db import models

class Lifter(models.Model):
    member_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Meet(models.Model):
    meet_id = models.AutoField(primary_key=True)
    meet_name = models.CharField(max_length=255)
    meet_date = models.DateField()

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Lifter, on_delete=models.CASCADE)
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    placing = models.IntegerField()
    division = models.CharField(max_length=255)
    bodyweight_kg = models.FloatField()
    weight_class_kg = models.IntegerField()
    squat1_kg = models.FloatField(null=True)
    squat2_kg = models.FloatField(null=True)
    squat3_kg = models.FloatField(null=True)
    bench1_kg = models.FloatField(null=True)
    bench2_kg = models.FloatField(null=True)
    bench3_kg = models.FloatField(null=True)
    deadlift1_kg = models.FloatField(null=True)
    deadlift2_kg = models.FloatField(null=True)
    deadlift3_kg = models.FloatField(null=True)
    total_kg = models.FloatField()
    points = models.FloatField()
    drug_tested = models.CharField(max_length=1)


# Seems like something I can improve, but trying to get it working before I worry about efficiency. Going to continue working on this after Capstone is done anyway.