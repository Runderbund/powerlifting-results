from rest_framework import serializers
from .models import Lifter, Meet, Result, Record

class LifterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifter
        fields = ['member_id', 'name']

class MeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meet
        fields = ['meet_id', 'meet_name', 'meet_date', 'location']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['result_id', 'lifter', 'meet', 'division', 'weight_class_kg', 'bodyweight_kg', 
                  'squat_1_kg', 'squat_2_kg', 'squat_3_kg',
                  'bench_1_kg', 'bench_2_kg', 'bench_3_kg',
                  'deadlift_1_kg', 'deadlift_2_kg', 'deadlift_3_kg',
                  'total_kg', 'points', 'drug_test', 'team', 'lot_number']

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['category', 'sex', 'discipline', 'weight_class', 'meet', 'lifter_name', 'lift_weight', 'date', 'bodyweight']

