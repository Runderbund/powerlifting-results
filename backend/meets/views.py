from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import csv
from .models import Lifter, Meet, Result


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            meet_name = form.cleaned_data.get('meet_name')
            meet_date = form.cleaned_data.get('meet_date')
            meet = Meet.objects.create(meet_name=meet_name, meet_date=meet_date)
            handle_uploaded_file(request.FILES["file"], meet)
            return HttpResponseRedirect("/success/url/")
    else:
        form = UploadFileForm()
        # Stay on same page, print out errors below.
    return render(request, "upload.html", {"form": form})



def handle_uploaded_file(f, meet):
    
    lifter_array = make_lifter_array(f, meet)

    for row in lifter_array:
        name, team, div, bodyweight_kg, weight_class, date_of_birth,  lot, squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3, discipline, state, member_id, drug_test = row.values()

        total_kg = calculate_total()
        placing = calculate_placing()
        points = calculate_points()
        sex, equipped, age_div = deconstruct_division(div)
        lifter = get_or_create_lifter(member_id, name)
        division = compare_dob_and_division(date_of_birth, division, meet.meet_date)


# Take in CSV file and returns an array of lifters.
def make_lifter_array(f, meet):
    lifter_array = []
    data = csv.reader(f)
    headers = next(data, None)  # Skips the headers
    for row in data:
        if not any(row):  # Stops taking in data when it hits the first blank row
            break
        lifter_dict = {}
        for i, value in enumerate(row):
            header = headers[i]
            if header.endswith("_kg"):
                if header == "weight_class_kg":
                    lifter_dict[header] = int(value) if value else None
                else:
                    lifter_dict[header] = float(value) if value else None
            elif header == "points":
                lifter_dict[header] = float(value) if value else None
            else:
                lifter_dict[header] = value
        lifter_dict["meet"] = meet
        lifter_array.append(lifter_dict)
    return lifter_array

# Gets a lifter from the database, or creates a new one.
def get_or_create_lifter(member_id, name):
    lifter, created = Lifter.objects.get_or_create(
        member_id=member_id,
        defaults={"name": name},
    )
    return lifter


# Takes the division apart for easier comparison where needed, e.g., age group and birthdate comparison.
def deconstruct_division(division):
    # Initialize the dictionary to store the components
    components = {}

    # Check first letter of division. If M, sex = male. If F, sex = female.
    if division[0] == "M":
        components["sex"] = "male"
    elif division[0] == "F":
        components["sex"] = "female"
    else:
        raise ValueError(f"Invalid division {division}. Must start with 'M' or 'F'.")

    # Check second letter of division. If R, equipment = raw. If nothing before dash, equipment = equipped.
    if division[1] == "R":
        components["equipment"] = "raw"
    else:
        components["equipment"] = "equipped"

    # Check after dash. age group = that (e.g. JR, M1, etc.)
    if "-" in division:
        components["age_group"] = division.split("-")[1]
    else:
        raise ValueError(
            f"Invalid division {division}. Must contain '-' followed by age group."
        )

    return components


# Adds best squat, bench, and deadlift together to calculate a lifter's total.
def calculate_total(lifter):
    squat_attempts = [lifter["squat1_kg"], lifter["squat2_kg"], lifter["squat3_kg"]]
    bench_attempts = [lifter["bench1_kg"], lifter["bench2_kg"], lifter["bench3_kg"]]
    deadlift_attempts = [
        lifter["deadlift1_kg"],
        lifter["deadlift2_kg"],
        lifter["deadlift3_kg"],
    ]

    # Filters out unsuccessful attempts, which are negative numbers in the CSV
    successful_squats = [attempt for attempt in squat_attempts if attempt >= 0]
    successful_benches = [attempt for attempt in bench_attempts if attempt >= 0]
    successful_deadlifts = [attempt for attempt in deadlift_attempts if attempt >= 0]

    # If there are no successful attempts for a lift, that lift is 0. Otherwise, it's the heaviest of the successful attempts.
    best_squat = max(successful_squats) if successful_squats else 0
    best_bench = max(successful_benches) if successful_benches else 0
    best_deadlift = max(successful_deadlifts) if successful_deadlifts else 0

    total = best_squat + best_bench + best_deadlift

    return total

# Check whether the lifter is in the correct division for their age. If not, they will be moved to the correct division prior to calculating placing and points.
# This is by year. E.g., in 2023, anyone born in 2000 is considered a 23 years old.
def compare_dob_and_division(date_of_birth, division, meet_date):
    _, age_div = deconstruct_division(division)

    # Calculates the lifter's age
    age_at_meet = meet_date.year - date_of_birth.year

    # Define the age groups with the minimum age for each
    age_groups = {"JR": 19, "M1": 40, "M2": 50, "M3": 60, "M4": 70, "M5": 80}

    # Check each age group in descending order
    for age_group in sorted(age_groups.keys(), key=age_groups.get, reverse=True):
        # Sorts the keys based on their values in the age_groups dictionary
        if age_at_meet >= age_groups[age_group]:
            correct_age_div = age_group
            break

    # If the lifter's division doesn't match their age, return the corrected division
    if age_div != "O" and age_div != correct_age_div:
        division = division.replace(age_div, correct_age_div)

    # TODO: Add logging

    return division


# Check whether the lifter is in the correct weight class for their bodyweight.
def compare_bodyweight_and_weightclass(sex, weight_class, bodyweight_kg):
    WEIGHT_CLASSES = {
        "W": {
            43.0: "43.0",
            47.0: "47.0",
            52.0: "52.0",
            57.0: "57.0",
            63.0: "63.0",
            69.0: "69.0",
            76.0: "76.0",
            84.0: "84.0",
            float("inf"): "84.0+",
        },
        "M": {
            53.0: "53.0",
            59.0: "59.0",
            66.0: "66.0",
            74.0: "74.0",
            83.0: "83.0",
            93.0: "93.0",
            105.0: "105.0",
            120.0: "120.0",
            float("inf"): "120.0+",
        },
    }

    for threshold in sorted(WEIGHT_CLASSES[sex]):
        if bodyweight_kg <= threshold:
            correct_weight_class = WEIGHT_CLASSES[sex][threshold]
            break

    if weight_class != correct_weight_class:
        return correct_weight_class
    else:
        return weight_class
    
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
    # Creates new result
    # Result.objects.create(
    #     lifter=lifter,
    #     team=team,
    #     meet=meet,
    #     placing=int(placing),
    #     division=div,
    #     bodyweight_kg=float(bwt_kg),
    #     weight_class_kg=int(ipf_wt_cls),
    #     date_of_birth=dob,
    #     lot=int(lot),
    #     squat1_kg=float(squat1) if squat1 else None,
    #     squat2_kg=float(squat2) if squat2 else None,
    #     squat3_kg=float(squat3) if squat3 else None,
    #     bench1_kg=float(bench1) if bench1 else None,
    #     bench2_kg=float(bench2) if bench2 else None,
    #     bench3_kg=float(bench3) if bench3 else None,
    #     deadlift1_kg=float(deadlift1) if deadlift1 else None,
    #     deadlift2_kg=float(deadlift2) if deadlift2 else None,
    #     deadlift3_kg=float(deadlift3) if deadlift3 else None,
    #     total_kg=total_kg,
    #     points=points,
    #     discipline=event,
    #     state=state,
    #     drug_tested=drug_test,
    # )
    pass


def upload_success():
    # If there is nothing that needs to be checked manually (e.g., dob in future), then this will just redirect to the next page, where changes will be displayed and the modified file will be available for download.
    pass
