from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
import csv
from .models import Lifter, Meet, Result
import pandas as pd
import math
import io
from rest_framework.decorators import api_view
from datetime import datetime, date
from django.http import JsonResponse
from .models import Lifter, Meet, Result


@api_view(["POST"])
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        meet_name = form.cleaned_data.get("meetName")
        meet_date = form.cleaned_data.get("meetDate")
        meet = Meet.objects.create(meet_name=meet_name, meet_date=meet_date)
        change_log = handle_uploaded_file(request.FILES["resultsFile"], meet)
        return JsonResponse(
            {
                "message": "File uploaded successfully",
                "meetId": meet.meet_id,
                "changeLog": change_log,
            }
        )
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


# Runs through each lifter in the CSV file and resolves conflicts.
# Then, assigns placing and points.
# Returns an updated array of lifters and results.
def handle_uploaded_file(f, meet):
    lifter_array = make_lifter_array(f, meet)
    processed_lifter_data = []
    age_div_changes = []
    weight_class_changes = []

    for row in lifter_array:
        (
            name,
            team,
            division,
            bodyweight,
            weight_class,
            date_of_birth,
            lot,
            squat1,
            squat2,
            squat3,
            bench1,
            bench2,
            bench3,
            deadlift1,
            deadlift2,
            deadlift3,
            discipline,
            state,
            member_id,
            drug_tested,
            meet,
        ) = row.values()

        total = calculate_total(
            squat1,
            squat2,
            squat3,
            bench1,
            bench2,
            bench3,
            deadlift1,
            deadlift2,
            deadlift3,
        )
        lifter = get_or_create_lifter(member_id, name)
        division, age_change = compare_dob_and_division(
            name, date_of_birth, division, meet.meet_date
        )

        division_components = deconstruct_division(division)
        sex = division_components["sex"]
        equipment = division_components["equipment"]
        age_group = division_components["age_group"]

        weight_class, weight_change = compare_bodyweight_and_weightclass(
            name, sex, weight_class, bodyweight
        )
        points = calculate_points(sex, equipment, discipline, total, bodyweight)

        if len(age_change) == 3:
            age_div_changes.append(age_change)
        if len(weight_change) == 3:
            weight_class_changes.append(weight_change)

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
        result = Result.objects.create(**lifter_data)  # Unpacks the dictionary
        result_objects.append(result)
    change_log = log_changes(age_div_changes, weight_class_changes)

    return change_log


# Take in CSV file and returns an array of lifters.
def make_lifter_array(f, meet):
    lifter_array = []
    data = csv.reader(io.TextIOWrapper(f, encoding="utf-8"))
    headers = next(data, None)  # Skips the headers
    for row in data:
        if not any(row):  # Stops taking in data when it hits the first blank row
            break
        lifter_dict = {}
        for i, value in enumerate(row):
            header = headers[i]
            if header == "DOB":
                lifter_dict[header] = (
                    datetime.strptime(value, "%m/%d/%Y").date() if value else None
                )
            elif header == "Bwt - kg" or header in [
                "Squat 1",
                "Squat 2",
                "Squat 3",
                "Bench 1",
                "Bench 2",
                "Bench 3",
                "Deadlift 1",
                "Deadlift 2",
                "Deadlift 3",
            ]:
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
def calculate_total(
    squat1, squat2, squat3, bench1, bench2, bench3, deadlift1, deadlift2, deadlift3
):
    squat_attempts = [squat1, squat2, squat3]
    bench_attempts = [bench1, bench2, bench3]
    deadlift_attempts = [deadlift1, deadlift2, deadlift3]

    # Filters out unsuccessful attempts, which are negative numbers in the CSV
    successful_squats = [
        attempt for attempt in squat_attempts if attempt is not None and attempt >= 0
    ]
    successful_benches = [
        attempt for attempt in bench_attempts if attempt is not None and attempt >= 0
    ]
    successful_deadlifts = [
        attempt for attempt in deadlift_attempts if attempt is not None and attempt >= 0
    ]

    # If there are no successful attempts for a lift, that lift is 0. Otherwise, it's the heaviest of the successful attempts.
    best_squat = max(successful_squats) if successful_squats else 0
    best_bench = max(successful_benches) if successful_benches else 0
    best_deadlift = max(successful_deadlifts) if successful_deadlifts else 0

    total = best_squat + best_bench + best_deadlift

    return total


# Check whether the lifter is in the correct division for their age. If not, they will be moved to the correct division prior to calculating placing and points.
# This is by year. E.g., in 2023, anyone born in 2000 is considered a 23 years old.
# TODO: Finish adjusting for sub-juniors
## Adjust to SJ if accidentally in J, vice/versa
def compare_dob_and_division(name, date_of_birth, division, meet_date):
    division_components = deconstruct_division(division)
    age_div = division_components["age_group"]

    # If the lifter's division is "O", no check is needed: returns the original division and an empty change list. 
    if age_div == "O":
        return division, []

    age_changes = []

    # Calculates the lifter's age
    age_delta = meet_date - date_of_birth
    age_at_meet = age_delta.days // 365  # Integer division to get the age in full years

    # Special case for Sub-Junior (SJ) classification
    # "Sub-Junior: from the day the lifter reaches 14 years and throughout the full calendar year in which the lifter reaches 18 years."
    if age_div == "SJ":
        sj_start_date = date(date_of_birth.year + 14, date_of_birth.month, date_of_birth.day)
        sj_end_date = date(date_of_birth.year + 18, 12, 31)
        
        if sj_start_date <= meet_date <= sj_end_date:
            return division, []
        else:
            # Reclassification logic
            age_changes = [name, age_div, "O"]
            division = division.replace(age_div, "O")
            return division, age_changes

    # Define the age groups with the minimum and maximum age for each
    age_groups = {
        "J": {"min": 19, "max": 23},
        "M1": {"min": 40, "max": 49},
        "M2": {"min": 50, "max": 59},
        "M3": {"min": 60, "max": 69},
        "M4": {"min": 70, "max": float('inf')},  # No upper limit for M4
    }

    correct_age_div = "O" # Default to Open division

    # Finds the correct age division based on DOB
    for age_group, age_range in age_groups.items():
        # Checks if the lifter's age is within the current age group's range
        if age_range["min"] <= age_at_meet < age_range["max"]:
            # Sets the correct age division to the current age group
            correct_age_div = age_group
            break

    # If the lifter's division doesn't match the correct age division, returns the corrected division
    if age_div != correct_age_div:
        age_changes = [name, age_div, correct_age_div]
        division = division.replace(age_div, correct_age_div)
    else:
        age_changes = []
    return division, age_changes



# Check whether the lifter is in the correct weight class for their bodyweight.
def compare_bodyweight_and_weightclass(name, sex, weight_class, bodyweight):
    WEIGHT_CLASSES = {
        "female": {
            "43": {"min": 0, "max": 43},
            "47": {"min": 43.1, "max": 47},
            "52": {"min": 47.1, "max": 52},
            "57": {"min": 52.1, "max": 57},
            "63": {"min": 57.1, "max": 63},
            "69": {"min": 63.1, "max": 69},
            "76": {"min": 69.1, "max": 76},
            "84": {"min": 76.1, "max": 84},
            "84+": {"min": 84.1, "max": float("inf")},
        },
        "male": {
            "53": {"min": 0, "max": 53},
            "59": {"min": 53.1, "max": 59},
            "66": {"min": 59.1, "max": 66},
            "74": {"min": 66.1, "max": 74},
            "83": {"min": 74.1, "max": 83},
            "93": {"min": 83.1, "max": 93},
            "105": {"min": 93.1, "max": 105},
            "120": {"min": 105.1, "max": 120},
            "120+": {"min": 120.1, "max": float("inf")},
        },
    }

    weight_changes = []

    correct_weight_class = "120+" if sex == "male" else "84+"

    for weight_class_key, weight_range in WEIGHT_CLASSES[sex].items():
        # If the lifter's bodyweight is within the current weight class's range
        if weight_range["min"] <= bodyweight <= weight_range["max"]:
            # Sets the correct weight class to the current weight class
            correct_weight_class = weight_class_key
            break

    if weight_class != correct_weight_class:
        weight_changes = [name, weight_class, correct_weight_class]
        weight_class = correct_weight_class

    return weight_class, weight_changes


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


def log_changes(age_div_changes, weight_class_changes):
    change_log = []

    # Logs the changes related to the age division
    for change in age_div_changes:
        if change:  # Ignore empty arrays
            lifter_name, original_age_div, correct_age_div = change
            change_log.append(
                f"For lifter {lifter_name}, age group did not match with date of birth. Adjusted age group from {original_age_div} to {correct_age_div}."
            )

    # Logs the changes related to the weight class
    for change in weight_class_changes:
        if change:
            lifter_name, original_weight_class, correct_weight_class = change
            change_log.append(
                f"For lifter {lifter_name}, weight class did not match with bodyweight. Adjusted weight class from {original_weight_class} kg to {correct_weight_class} kg."
            )

    # Checks if any changes were made
    if len(change_log) > 0:
        # Start of the message
        change_log.insert(
            0, "The following changes were made to the results that were provided.\n"
        )
        # End of the message
        change_log.append("\nPlease see the attached CSV file.")
    else:
        change_log.append(
            "There were no changes to the provided data. All age groups matched birth dates and all weight classes matched bodyweight."
        )

    return change_log


# Writing all for now. Adjust to only neccessary fields later and put in order.
# Check with Dad to see what he uploads.
def download_meet_results(request, meet_id):
    # Gets the results for the specified meet
    results = Result.objects.filter(meet__meet_id=meet_id).values(
        "lifter__name",
        "lifter__member_id",
        "team",
        "division",
        "sex",
        "equipment",
        "age_group",
        "bodyweight",
        "weight_class",
        "date_of_birth",
        "lot",
        "squat1",
        "squat2",
        "squat3",
        "bench1",
        "bench2",
        "bench3",
        "deadlift1",
        "deadlift2",
        "deadlift3",
        "total",
        "discipline",
        "points",
        "state",
        "placing",
        "drug_tested",
    )

    # Prepares the HttpResponse object with appropriate CSV headers.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="meet_results.csv"'

    # Writes the data to the response object
    writer = csv.writer(response)
    writer.writerow(
        [
            "Name",
            "Member ID",
            "Team",
            "Division",
            "Sex",
            "Equipment",
            "Age Group",
            "Bodyweight",
            "Weight Class",
            "Date of Birth",
            "Lot",
            "Squat1",
            "Squat2",
            "Squat3",
            "Bench1",
            "Bench2",
            "Bench3",
            "Deadlift1",
            "Deadlift2",
            "Deadlift3",
            "Total",
            "Discipline",
            "Points",
            "State",
            "Placing",
            "Drug Tested",
        ]
    )
    for result in results:
        writer.writerow(result.values())

    return response


def list_lifters(request):
    lifters = Lifter.objects.all().order_by("name").values("member_id", "name")
    return JsonResponse({"lifters": list(lifters)})


def lifter_detail(request, lifter_id):
    lifter = Lifter.objects.filter(member_id=lifter_id).values()
    results = Result.objects.filter(lifter__member_id=lifter_id).values(
        "meet__meet_id",
        "meet__meet_name",
        "meet__meet_date",
        "placing",
        "division",
        "bodyweight",
        "weight_class",
        "squat1",
        "squat2",
        "squat3",
        "bench1",
        "bench2",
        "bench3",
        "deadlift1",
        "deadlift2",
        "deadlift3",
        "total",
        "points",
    )
    return JsonResponse({"lifter": list(lifter), "results": list(results)})


def list_meets(request):
    meets = Meet.objects.all().values("meet_id", "meet_name")
    return JsonResponse({"meets": list(meets)})


def meet_results(request, meet_id):
    meet = Meet.objects.get(pk=meet_id)
    results = meet.result_set.values(
        "lifter__name",
        "lifter__member_id",
        "placing",
        "division",
        "bodyweight",
        "weight_class",
        "squat1",
        "squat2",
        "squat3",
        "bench1",
        "bench2",
        "bench3",
        "deadlift1",
        "deadlift2",
        "deadlift3",
        "total",
        "points",
    )
    meet_data = {"meet_name": meet.meet_name, "meet_date": meet.meet_date}
    return JsonResponse({"meet": meet_data, "results": list(results)})
