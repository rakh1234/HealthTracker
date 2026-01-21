from rest_framework import serializers
from .models import Activity, NutritionEntry, UserGoal


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id', 'activity_type', 'duration', 'distance',
            'calories_burned', 'date', 'notes'
        ]
        read_only_fields = ['id']


class NutritionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionEntry
        fields = [
            'id', 'food_name', 'calories', 'protein', 'carbs',
            'fat', 'quantity', 'date', 'meal_type'
        ]
        read_only_fields = ['id']


class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = [
            'id', 'goal_type', 'target_weight', 'target_calories_burn',
            'target_calories_consume', 'target_protein',
            'target_activity_days'
        ]
        read_only_fields = ['id']