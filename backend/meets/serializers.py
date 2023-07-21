from rest_framework import serializers
from .models import Lifter, Meet, Result, Record


class LifterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifter
        fields = ["member_id", "name"]


class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = ["meet_id", "meet_name", "meet_date"]

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = [
            "result_id",
            "meet",
            "lifter",
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
        ]




class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = [
            "id",
            "division",
            "discipline",
            "weight_class_kg",
            "meet",
            "lifter",
            "lift_weight_kg",
            "date",
        ]
