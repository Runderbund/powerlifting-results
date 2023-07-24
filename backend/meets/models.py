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

SEX_CHOICES = (
    ('M', 'male'),
    ('F', 'female')
)

EQUIPMENT_CHOICES = (
    ('E', 'equipped'),
    ('R', 'raw')
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

# Not currently used
class Record(models.Model):
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES, null=True)
    discipline = models.CharField(max_length=2, choices=DISCIPLINE_CHOICES, null=True)
    weight_class_kg = models.IntegerField()
    meet = models.ForeignKey(Meet, on_delete=models.PROTECT, null=True)
    lifter = models.ForeignKey(Lifter, on_delete=models.PROTECT, null=True)
    lift_weight_kg = models.FloatField()
    date = models.DateField()

# Added null=True to all fields to avoid errors. Adjust later once I figure out main areas.
class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    meet = models.ForeignKey(Meet, on_delete=models.CASCADE, null=True)
    lifter = models.ForeignKey(Lifter, on_delete=models.CASCADE, null=True)
        # instead of name and member_id. Linked to lifter, which includes both
        # Not sure how to handle listing results for individual lifter efficiently. Current plan involves matching across all results for member_id, but this involves checking the whole thing every time a lifter page loads.
    team = models.CharField(max_length=255, null=True)
    division = models.CharField(max_length=5, choices=DIVISION_CHOICES, null=True)
    sex = models.CharField(max_length=100, choices=SEX_CHOICES, null=True)
    equipment = models.CharField(max_length=100, choices=EQUIPMENT_CHOICES, null=True)
    age_group = models.CharField(max_length=200, null=True)
    bodyweight = models.FloatField(null=True)
    weight_class = models.CharField(max_length=5, null=True)
    date_of_birth = models.DateField(null=True)
    lot = models.IntegerField(null=True)
    squat1 = models.FloatField(null=True)
    squat2 = models.FloatField(null=True)
    squat3 = models.FloatField(null=True)
    bench1 = models.FloatField(null=True) 
    bench2 = models.FloatField(null=True)
    bench3 = models.FloatField(null=True)
    deadlift1 = models.FloatField(null=True)
    deadlift2 = models.FloatField(null=True) 
    deadlift3 = models.FloatField(null=True)
    total = models.FloatField(null=True)
    discipline = models.CharField(max_length=2, choices=DISCIPLINE_CHOICES, null=True)
    points = models.FloatField(null=True)
    state = models.CharField(max_length=2, null=True)
    placing = models.IntegerField(null=True)
    drug_tested = models.CharField(max_length=1, null=True) # Could add Y/N as choices