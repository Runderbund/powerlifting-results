from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
import csv
from .models import Lifter, Meet, Result
import pandas as pd  # Learn more about pandas
import math
import io
# from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime
from django.http import JsonResponse
from .models import Lifter, Meet, Result



# @permission_classes([IsAuthenticated])
# Needed? Button is only there when logged in, and already diverts to login page if not logged in.

@api_view(['POST'])
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        meet_name = form.cleaned_data.get('meetName')
        meet_date = form.cleaned_data.get('meetDate')
        meet = Meet.objects.create(meet_name=meet_name, meet_date=meet_date)
        result_objects = handle_uploaded_file(request.FILES["resultsFile"], meet)
        return HttpResponse("File uploaded successfully")
    else:
        form = UploadFileForm()
        # Stay on same page, print out errors below.
    return render(request, "upload.html", {"form": form})



# Runs through each lifter in the CSV file and resolves conflicts.
# Then, assigns placing and points.
# Returns an updated array of lifters and results.
def handle_uploaded_file(f, meet):
    lifter_array = make_lifter_array(f, meet)
    processed_lifter_data = []

    for row in lifter_array:
        name, team, division, bodyweight, weight_class, date_of_birth, lot, squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3, discipline, state, member_id, drug_tested, meet = row.values()

        division_components = deconstruct_division(division)
        sex = division_components['sex']
        equipment = division_components['equipment']
        age_group = division_components['age_group']

        total = calculate_total(squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3)
        lifter = get_or_create_lifter(member_id, name)
        division = compare_dob_and_division(date_of_birth, division, meet.meet_date)
        points = calculate_points(sex, equipment, discipline, total, bodyweight)

        processed_lifter_data.append(
            {
                "meet": meet,
                "lifter": lifter,
                "team": team,
                "division": division,
                "bodyweight": bodyweight,
                "weight_class": weight_class,
                "date_of_birth": date_of_birth,
                "lot": lot,
                "squat1": squat1,
                "squat2": squat2,
                "squat3": squat3,
                "bench1": bench1,
                "bench2": bench2,
                "bench3": bench3,
                "deadlift1": deadlift1,
                "deadlift2": deadlift2,
                "deadlift3": deadlift3,
                "total": total,
                "discipline": discipline,
                "state": state,
                "drug_tested": drug_tested,
                "sex": sex,
                "equipment": equipment,
                "age_group": age_group,
                "points": points,
            }
        )

    processed_lifter_data = calculate_placing(processed_lifter_data)
    result_objects = []
    for lifter_data in processed_lifter_data:
        result = Result.objects.create(**lifter_data) # Unpacks the dictionary
        result_objects.append(result)
        # Create Lifter, Meet, and Record objects

    return result_objects



# Take in CSV file and returns an array of lifters.
def make_lifter_array(f, meet):
    lifter_array = []
    data = csv.reader(io.TextIOWrapper(f, encoding='utf-8'))
    headers = next(data, None)  # Skips the headers
    for row in data:
        if not any(row):  # Stops taking in data when it hits the first blank row
            break
        lifter_dict = {}
        for i, value in enumerate(row):
            header = headers[i]
            if header == 'DOB':
                lifter_dict[header] = datetime.strptime(value, "%m/%d/%Y").date() if value else None
            elif header == 'Bwt - kg' or header in ['Squat 1', 'Squat 2', 'Squat 3', 'Bench 1', 'Bench 2', 'Bench 3', 'Deadlift 1', 'Deadlift 2', 'Deadlift 3']:
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
def calculate_total(squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3):
    squat_attempts = [squat1, squat2, squat3]
    bench_attempts = [bench1, bench2, bench3]
    deadlift_attempts = [deadlift1, deadlift2, deadlift3]

    # Filters out unsuccessful attempts, which are negative numbers in the CSV
    successful_squats = [attempt for attempt in squat_attempts if attempt is not None and attempt >= 0]
    successful_benches = [attempt for attempt in bench_attempts if attempt is not None and attempt >= 0]
    successful_deadlifts = [attempt for attempt in deadlift_attempts if attempt is not None and attempt >= 0]


    # If there are no successful attempts for a lift, that lift is 0. Otherwise, it's the heaviest of the successful attempts.
    best_squat = max(successful_squats) if successful_squats else 0
    best_bench = max(successful_benches) if successful_benches else 0
    best_deadlift = max(successful_deadlifts) if successful_deadlifts else 0

    total = best_squat + best_bench + best_deadlift

    return total


# Check whether the lifter is in the correct division for their age. If not, they will be moved to the correct division prior to calculating placing and points.
# This is by year. E.g., in 2023, anyone born in 2000 is considered a 23 years old.
def compare_dob_and_division(date_of_birth, division, meet_date):
    _, _, age_div = deconstruct_division(division)

    # Calculates the lifter's age
    age_at_meet = meet_date.year - date_of_birth.year

    # Define the age groups with the minimum age for each
    age_groups = {"JR": 19, "M1": 40, "M2": 50, "M3": 60, "M4": 70, "M5": 80}

    # Avoids error on last if check
    correct_age_div = "O"
    
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
    # TODO: Handle Subjunior and below

    return division


# Check whether the lifter is in the correct weight class for their bodyweight.
def compare_bodyweight_and_weightclass(sex, weight_class, bodyweight_kg):
    WEIGHT_CLASSES = {
        "W": {
            43.0: "43",
            47.0: "47",
            52.0: "52",
            57.0: "57",
            63.0: "63",
            69.0: "69",
            76.0: "76",
            84.0: "84",
            float("inf"): "84+",
        },
        "M": {
            53.0: "53",
            59.0: "59",
            66.0: "66",
            74.0: "74",
            83.0: "83",
            93.0: "93",
            105.0: "105",
            120.0: "120",
            float("inf"): "120+",
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


# Compares the totals within each division (sex, age group, weight class) and assigns a placing (1st, 2nd, 3rd, etc.)
# Double check how to handle ties. Bodyweight, or lot number?
# For now, assigns same rank to ties
def calculate_placing(lifter_data):
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(lifter_data)

    # Calculate the placings within each division and weight class
    df["placing"] = df.groupby(["division", "weight_class"])["total"].rank(
        ascending=False, method="min"
    )

    # Convert the placings to integers
    df["placing"] = df["placing"].astype(int)

    # Convert the DataFrame back to a list of dictionaries
    lifter_data = df.to_dict("records")

    return lifter_data


# Calculates IPF GoodLift points
def calculate_points(sex, equipped, discipline, total, bodyweight):
    # Defines the coefficients for the points calculation
    COEFFICIENTS = {
        "male": {
            "equipped PL": [1236.25115, 1449.21864, 0.01644],
            "raw PL": [1199.72839, 1025.18162, 0.00921],
            "equipped BP": [381.22073, 733.79378, 0.02398],
            "raw BP": [320.98041, 281.40258, 0.01008],
        },
        "female": {
            "equipped PL": [758.63878, 949.31382, 0.02435],
            "raw PL": [610.32796, 1045.59282, 0.03048],
            "equipped BP": [221.82209, 357.00377, 0.02937],
            "raw BP": [142.40398, 442.52671, 0.04724],
        },
    }

    # Uses the correct coefficients based on the sex, equipment, and discipline
    coefficients = COEFFICIENTS[sex][f"{equipped} {discipline}"]
    A, B, C = coefficients

    points = round(100 / (A - B * (math.exp(-C * bodyweight))) * total, 2)

    return points


# TODO: Add Dl/PP events


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


#  Not needed with for snippet at bottom of handle_uploaded_file
# def create_result_objects(processed_lifter_data, meet):
#     result_objects = []
#     for data in processed_lifter_data:
#         result = Result(
#             meet=data["meet"],
#             lifter=data["lifter"],
#             team=data["team"],
#             division=data["division"],
#             bodyweight=data["bodyweight"],
#             weight_class=data["weight_class"],
#             date_of_birth=data["date_of_birth"],
#             lot=data["lot"],
#             squat1=data.get("squat1"),
#             squat2=data.get("squat2"),
#             squat3=data.get("squat3"),
#             bench1=data.get("bench1"),
#             bench2=data.get("bench2"),
#             bench3=data.get("bench3"),
#             deadlift1=data.get("deadlift1"),
#             deadlift2=data.get("deadlift2"),
#             deadlift3=data.get("deadlift3"),
#             total=data["total"],
#             discipline=data["discipline"],
#             state=data["state"],
#             member_id=data["member_id"],
#             drug_test=data["drug_test"],
#             sex=data["sex"],
#             equipment=data["equipment"],
#             age_group=data["age_group"],
#             points=data["points"],
#         )
#         result.save()
#         result_objects.append(result)
#     return result_objects



def upload_success():
    # If there is nothing that needs to be checked manually (e.g., dob in future), then this will just redirect to the next page, where changes will be displayed and the modified file will be available for download.
    pass


def list_lifters(request):
    lifters = Lifter.objects.all().order_by('name').values('member_id', 'name')
    return JsonResponse({'lifters': list(lifters)})


# def lifter_detail(request, lifter_id):
#     lifter = Lifter.objects.filter(member_id=lifter_id).values()
#     results = Result.objects.filter(lifter__member_id=lifter_id).values()
#     return JsonResponse({'lifter': list(lifter), 'results': list(results)})

def lifter_detail(request, lifter_id):
    lifter = Lifter.objects.filter(member_id=lifter_id).values()
    results = Result.objects.filter(lifter__member_id=lifter_id).values('meet__meet_name', 'meet__meet_date', 'placing', 'division', 'bodyweight', 'squat1', 'squat2', 'squat3', 'bench1', 'bench2', 'bench3', 'deadlift1', 'deadlift2', 'deadlift3', 'total', 'points')
    return JsonResponse({'lifter': list(lifter), 'results': list(results)})



def list_meets(request):
    meets = Meet.objects.all().values('meet_id', 'meet_name')
    return JsonResponse({'meets': list(meets)})

# def meet_results(request, meet_id):
#     meet = Meet.objects.filter(meet_id=meet_id).values()
#     results = Result.objects.filter(meet__meet_id=meet_id).values()
#     return JsonResponse({'meet': list(meet), 'results': list(results)})

# def meet_results(request, meet_id):
#     meet = Meet.objects.get(pk=meet_id)
#     results = meet.result_set.values('lifter__name', 'placing', 'division', 'bodyweight', 'squat1', 'squat2', 'squat3', 'bench1', 'bench2', 'bench3', 'deadlift1', 'deadlift2', 'deadlift3', 'total', 'points')
#     return JsonResponse({'meet': meet, 'results': list(results)})

def meet_results(request, meet_id):
    meet = Meet.objects.get(pk=meet_id)
    results = meet.result_set.values('lifter__name', 'placing', 'division', 'bodyweight', 'squat1', 'squat2', 'squat3', 'bench1', 'bench2', 'bench3', 'deadlift1', 'deadlift2', 'deadlift3', 'total', 'points')
    meet_data = {'meet_name': meet.meet_name, 'meet_date': meet.meet_date}  # Adjust this line to match your actual Meet model's fields.
    return JsonResponse({'meet': meet_data, 'results': list(results)})
