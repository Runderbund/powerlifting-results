from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import csv
from .models import Lifter, Meet, Result

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f, meet):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with open('some/file/name.txt', 'r') as file:
        data = csv.reader(file)
        headers = next(data, None) # Skips the headers
        for row in data:
            name, team, div, bwt_kg, ipf_wt_cls, dob, lot, squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3, event, state, member_id, drug_test = row
            # Create array
            # Compare for placing
            
            # Creates a new lifter if not already in database
            lifter, created = Lifter.objects.get_or_create(
                member_id=member_id,
                defaults={'name': name},
            )

            total_kg = (calculate_total())
            placing = (calculate_placing())
            points = (calculate_points())


            # Creates new result
            Result.objects.create(
                lifter=lifter,
                team=team,
                meet=meet,
                placing=int(placing),
                division=div,
                bodyweight_kg=float(bwt_kg),
                weight_class_kg=int(ipf_wt_cls),
                date_of_birth=dob,
                lot=int(lot),
                squat1_kg=float(squat1) if squat1 else None,
                squat2_kg=float(squat2) if squat2 else None,
                squat3_kg=float(squat3) if squat3 else None,
                bench1_kg=float(bench1) if bench1 else None,
                bench2_kg=float(bench2) if bench2 else None,
                bench3_kg=float(bench3) if bench3 else None,
                deadlift1_kg=float(deadlift1) if deadlift1 else None,
                deadlift2_kg=float(deadlift2) if deadlift2 else None,
                deadlift3_kg=float(deadlift3) if deadlift3 else None,
                total_kg=total_kg,
                points=points,
                discipline=event,
                state=state,
                drug_tested=drug_test,
            )


def make_lifter_array(f, meet):
    # Take in CSV file (provided by upload form), and meet (provided through:
    # class Meet(models.Model): 
        # meet_id = models.AutoField(primary_key=True)
        # meet_name = models.CharField(max_length=255)
        # meet_date = models.DateField()
            # Name and date come from textboxes outside of CSV (for now).)

    #  Stop taking in data at blank row. Only grab the top section of each CSV.

    # Creates an array of each row (minus the headers)
    # Each row represents one lifter and the information about them for this meet.
    pass

def deconstruct_division():
    # Check first letter of division. If M, sex = male. If F, sex = female.
    # Check second letter of division. If R, equipment = raw. If nothing before dash, equipment = equipped.
    # Check after dash. age group = that (e.g. JR, M1, etc.)

    # Should make it easier to update if needed, as well as calculate based on sex, equipment, and age group.
    pass

def upload_success():
    # If there is nothing that needs to be checked manually (e.g., dob in future), then this will just redirect to the next page, where changes will be displayed and the modified file will be available for download.
    pass

def calculate_total():
    # Adds best squat, bench, and deadlift together
    # Anything with - (e.g. "-125") is an unsuccesful lift and should not be counted.
    pass

def calculate_placing():
    # Compares the totals within each division (sex, age group, weight class) and assigns a placing (1st, 2nd, 3rd, etc.)
    # Later, be more specific, e.g., handle ties explicitly.
    pass

def calculate_points():
    # Calculate IPF GoodLift points
    # 100 / (A-B*e^(-C*bodyweight_kg))
    # Different A, B, and C based on division
    #                       A           B           C
    # Men’ s
    # Equipped Powerlifting 1236.25115  1449.21864  0.01644
    # Raw Powerlifting      1199.72839  1025.18162  0.00921
    # Equipped Bench Press  381.22073   733.79378   0.02398
    # Raw Bench Press       320.98041   281.40258   0.01008

    # Women’ s
    # Equipped Powerlifting 758.63878   949.31382   0.02435
    # Raw Powerlifting      610.32796   1045.59282  0.03048
    # Equipped Bench Press  221.82209   357.00377   0.02937
    # Raw Bench Press       142.40398   442.52671   0.04724
    pass

def compare_dob_and_division():
    # Check whether the lifter is in the correct division for their age, based on date_of_birth and meet_date.
    # This is by year. E.g., in 2023, anyone born in 2000 is considered a 23 years old.
        # i.e. "Master I: from 1 January in the calendar year the lifter reaches 40 years and throughout the full calendar year in which the lifter reaches 49 years."
        #  Junior  19-23
        #  Open  14+ (Lifters can compete in Open and/or their specific age group
        #  Master I  40-49
        #  Master II  50-59
        #  Master III  60-69
        #  Master IV  70-79
        #  Master V  80+
    # If the lifter is entered in the wrong division, they will be moved to the correct division prior to calculating placing and points.
    pass

def compare_bodyweight_and_weightclass():
    # Check whether the lifter is in the correct weight class for their bodyweight.

    # Women
    # 43.0 kg class up to 43.0 kg *
    # 47.0 kg class up to 47.0 kg **
    # 52.0 kg class from 47.01 kg up to 52.0 kg
    # 57.0 kg class from 52.01 kg up to 57.0 kg
    # 63.0 kg class from 57.01 kg up to 63.0 kg
    # 69.0 kg class from 63.01 kg up to 69.0 kg
    # 76.0 kg class from 69.01 kg up to 76.0 kg
    # 84.0 kg class from 76.01 kg up to 84.0 kg
    # 84.0+ kg class from 84.01 kg up to unlimited

    # Men
    # 53.0 kg class up to 53.0 kg *
    # 59.0 kg class up to 59.0 kg **
    # 66.0 kg class from 59.01 kg up to 66.0 kg
    # 74.0 kg class from 66.01 kg up to 74.0 kg
    # 83.0 kg class from 74.01 kg up to 83.0 kg
    # 93.0 kg class from 83.01 kg up to 93.0 kg
    # 105.0 kg class from 93.01 kg up to 105.0 kg
    # 120.0 kg class from 105.01 kg up to 120.0 kg
    # 120.0+ kg class from 120.01 kg up to unlimited

    pass

def check_for_new_records():
    # Compare to matching division and lift in Records. Update if higher.
    # Should check after each lift, technically, since records can be gained and lost to the next lifter prior to meet ending, and the lifter still gets credit for setting it.
        # Start by comparing largest in division, check in depth later.
    pass

def compare_name_and_member_id():
    # Check whether the name matches the member_id. If not, add to a log of errors and  send back to upload page.
    pass

def log_changes():
    # Every time a change is made, log it to a file.
    # For lifter [lifter name], age group did not match with date of birth. Adjusted age group from [age group] to [age group].
    # For lifter [lifter name], weight class did not match with bodyweight. Adjusted weight class from [weight class] to [weight class].
    # Lifter [lifter name] set a new record in [division] [lift] with [lift weight] kg.
    pass

def create_result_object(lifter_array):
    # After checks are done, created a Result object for each lifter.
    pass