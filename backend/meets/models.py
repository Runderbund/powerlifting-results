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

# Limit input choices to only valid options. Display full name of choice instead of abbreviation.
CATEGORY_CHOICES = (
    ('SJ', 'Sub Junior'),
    ('JR', 'Junior'),
    ('O', 'Open'),
    ('M1', 'Masters 1'),
    ('M2', 'Masters 2'),
    ('M3', 'Masters 3'),
    ('M4', 'Masters 4'),
    ('M5', 'Masters 5'),  
)

DISCIPLINE_CHOICES = (
    ('S', 'Squat'),
    ('B', 'Bench'),
    ('D', 'Deadlift'),
    ('T', 'Total'),  
    ('BS', 'Bench Single Lift')
)
   
class Record(models.Model):
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    sex = models.CharField(max_length=1)
    discipline = models.CharField(max_length=2, choices=DISCIPLINE_CHOICES)
    weight_class = models.IntegerField()
    meet = models.ForeignKey(Meet, on_delete=models.PROTECT) # Disallow deletion of meet if it has records associated with it.
    lifter_name = models.CharField(max_length=50)
    lift_weight = models.FloatField()
    date = models.DateField()
    bodyweight = models.FloatField()


# Seems like something I can improve, but trying to get it working before I worry about efficiency. Going to continue working on this after Capstone is done anyway.