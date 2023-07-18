from django.db import models

# Limit input choices to only valid options. Display full name of choice instead of abbreviation.
# Want to eventually limit to drop-downs on Entry form, but out of scope for now.
DIVISION_CHOICES = (
    ('MR-SJ', 'Male Raw - Sub Junior'),
    ('MR-JR', 'Male Raw - Junior'),
    ('MR-O', 'Male Raw - Open'), 
    ('MR-M1', 'Male Raw - Masters 1'),
    ('MR-M2', 'Male Raw - Masters 2'),
    ('MR-M3', 'Male Raw - Masters 3'),
    ('MR-M4', 'Male Raw - Masters 4'),
    ('MR-M5', 'Male Raw - Masters 5'),

    ('M-SJ', 'Male Equipped - Sub Junior'),
    ('M-JR', 'Male Equipped - Junior'), 
    ('M-O', 'Male Equipped - Open'),
    ('M-M1', 'Male Equipped - Masters 1'), 
    ('M-M2', 'Male Equipped - Masters 2'),
    ('M-M3', 'Male Equipped - Masters 3'),
    ('M-M4', 'Male Equipped - Masters 4'),
    ('M-M5', 'Male Equipped - Masters 5'),

    ('FR-SJ', 'Female Raw - Sub Junior'),
    ('FR-JR', 'Female Raw - Junior'),
    ('FR-O', 'Female Raw - Open'),
    ('FR-M1', 'Female Raw - Masters 1'),
    ('FR-M2', 'Female Raw - Masters 2'),
    ('FR-M3', 'Female Raw - Masters 3'),
    ('FR-M4', 'Female Raw - Masters 4'),
    ('FR-M5', 'Female Raw - Masters 5'),

    ('F-SJ', 'Female Equipped - Sub Junior'),
    ('F-JR', 'Female Equipped - Junior'),
    ('F-O', 'Female Equipped - Open'),
    ('F-M1', 'Female Equipped - Masters 1'),
    ('F-M2', 'Female Equipped - Masters 2'), 
    ('F-M3', 'Female Equipped - Masters 3'),
    ('F-M4', 'Female Equipped - Masters 4'),
    ('F-M5', 'Female Equipped - Masters 5'),
)

DISCIPLINE_CHOICES = (
    ('S', 'Squat'),
    ('B', 'Bench press'),
    ('D', 'Deadlift'),
    ('T', 'Total'),  
    ('BP', 'Bench press single lift')
)

class Lifter(models.Model):
    member_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    
class Meet(models.Model): 
    meet_id = models.AutoField(primary_key=True)
    meet_name = models.CharField(max_length=255)
    meet_date = models.DateField()
    # Name and date come from textboxes outside of CSV (for now).
    # Eventually State/Location and Sanction #, not important for now.

class Record(models.Model):
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES, null=True)
    discipline = models.CharField(max_length=2, choices=DISCIPLINE_CHOICES, null=True)
    weight_class_kg = models.IntegerField()
    meet = models.ForeignKey(Meet, on_delete=models.PROTECT, null=True)
    lifter = models.ForeignKey(Lifter, on_delete=models.PROTECT, null=True)
    lift_weight_kg = models.FloatField()
    date = models.DateField()

class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    lifter = models.ForeignKey(Lifter, on_delete=models.CASCADE)
    team = models.CharField(max_length=255)
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE)
    placing = models.IntegerField()
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES, null=True)
    bodyweight_kg = models.FloatField()
    weight_class_kg = models.IntegerField()
    date_of_birth = models.DateField()
    lot = models.IntegerField()
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
    discipline = models.CharField(max_length=2, choices=DISCIPLINE_CHOICES, null=True)
    state = models.CharField(max_length=2)
    drug_tested = models.CharField(max_length=1)