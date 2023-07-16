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
            "member",
            "meet",
            "division",
            "weight_class_kg",
            "bodyweight_kg",
            "squat1_kg",
            "squat2_kg",
            "squat3_kg",
            "bench1_kg",
            "bench2_kg",
            "bench3_kg",
            "deadlift1_kg",
            "deadlift2_kg",
            "deadlift3_kg",
            "total_kg",
            "points",
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
            "bodyweight_kg",
            "lift_weight_kg",
            "date",
        ]
