from django import forms
from .models import Activity, NutritionEntry, UserGoal


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'activity_type', 'duration', 'distance',
            'calories_burned', 'date', 'notes'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class NutritionEntryForm(forms.ModelForm):
    class Meta:
        model = NutritionEntry
        fields = [
            'food_name', 'calories', 'protein', 'carbs',
            'fat', 'quantity', 'date', 'meal_type'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserGoalForm(forms.ModelForm):
    class Meta:
        model = UserGoal
        fields = [
            'goal_type', 'target_weight', 'target_calories_burn',
            'target_calories_consume', 'target_protein',
            'target_activity_days'
        ]
        widgets = {
            'target_weight': forms.NumberInput(attrs={'step': '0.1'}),
            'target_protein': forms.NumberInput(attrs={'step': '0.1'}),
        }