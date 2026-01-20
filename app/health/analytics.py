from datetime import datetime, timedelta
from django.db.models import Sum, Avg, Count
from .models import Activity, NutritionEntry, UserGoal
import io
import base64

# Try to import optional packages
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Try to import numpy
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

def get_user_data(user, days=30):
    """Get user's activity and nutrition data for the last N days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    activities = Activity.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'duration', 'calories_burned', 'distance')

    nutrition = NutritionEntry.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'calories', 'protein', 'carbs', 'fat')

    return list(activities), list(nutrition)

def calculate_trends(activities, nutrition, days=30):
    """Calculate trends and averages"""
    if not activities and not nutrition:
        return {
            'avg_daily_calories_burned': 0,
            'avg_daily_calories_consumed': 0,
            'avg_daily_protein': 0,
            'avg_activity_days': 0,
            'trend_calories_burned': 0,
            'trend_calories_consumed': 0,
        }

    # Calculate averages
    total_burned = sum(a.get('calories_burned', 0) for a in activities)
    total_consumed = sum(n.get('calories', 0) for n in nutrition)
    total_protein = sum(n.get('protein', 0) for n in nutrition)

    avg_daily_calories_burned = total_burned / days if activities else 0
    avg_daily_calories_consumed = total_consumed / days if nutrition else 0
    avg_daily_protein = total_protein / days if nutrition else 0

    # Calculate activity days (unique dates with activity)
    activity_dates = set(a['date'] for a in activities if a.get('duration', 0) > 0)
    avg_activity_days = len(activity_dates) / (days / 7)  # per week

    # Simple trend calculation (comparing first half vs second half)
    mid_point = days // 2
    first_half_activities = [a for a in activities if (datetime.now().date() - a['date']).days >= mid_point]
    second_half_activities = [a for a in activities if (datetime.now().date() - a['date']).days < mid_point]

    first_half_burned = sum(a.get('calories_burned', 0) for a in first_half_activities)
    second_half_burned = sum(a.get('calories_burned', 0) for a in second_half_activities)

    total_activities = len(first_half_activities) + len(second_half_activities)
    trend_calories_burned = (second_half_burned - first_half_burned) / max(1, total_activities)

    first_half_nutrition = [n for n in nutrition if (datetime.now().date() - n['date']).days >= mid_point]
    second_half_nutrition = [n for n in nutrition if (datetime.now().date() - n['date']).days < mid_point]

    first_half_consumed = sum(n.get('calories', 0) for n in first_half_nutrition)
    second_half_consumed = sum(n.get('calories', 0) for n in second_half_nutrition)

    total_nutrition = len(first_half_nutrition) + len(second_half_nutrition)
    trend_calories_consumed = (second_half_consumed - first_half_consumed) / max(1, total_nutrition)

    return {
        'avg_daily_calories_burned': round(avg_daily_calories_burned, 1),
        'avg_daily_calories_consumed': round(avg_daily_calories_consumed, 1),
        'avg_daily_protein': round(avg_daily_protein, 1),
        'avg_activity_days': round(avg_activity_days, 1),
        'trend_calories_burned': round(trend_calories_burned, 2),
        'trend_calories_consumed': round(trend_calories_consumed, 2),
    }

def generate_activity_chart(activities, days=30):
    """Generate activity chart for the last N days - simplified version without matplotlib"""
    if not activities:
        return None

    # Create a simple text-based chart representation
    try:
        # Group activities by date
        date_totals = {}
        for activity in activities:
            date = activity['date']
            if date not in date_totals:
                date_totals[date] = 0
            date_totals[date] += activity.get('calories_burned') or 0

        # Sort by date
        sorted_dates = sorted(date_totals.keys())
        if not sorted_dates:
            return None

        # Create a simple ASCII chart
        max_calories = max(date_totals.values()) if date_totals else 0
        chart_lines = ["Daily Calories Burned (Last {} days):".format(days)]

        for date in sorted_dates[-min(days, len(sorted_dates)):]:  # Last N days
            calories = date_totals[date]
            bar_length = int((calories / max(max_calories, 1)) * 20)  # Scale to 20 chars
            bar = "█" * bar_length
            chart_lines.append(f"{date}: {bar} ({calories} cal)")

        return "\n".join(chart_lines)
    except Exception as e:
        print(f"Error generating activity chart: {e}")
        return None

def generate_nutrition_chart(nutrition, days=30):
    """Generate nutrition chart for the last N days - simplified version without matplotlib"""
    if not nutrition:
        return None

    try:
        # Group nutrition by date
        date_totals = {}
        for entry in nutrition:
            date = entry['date']
            if date not in date_totals:
                date_totals[date] = 0
            date_totals[date] += entry.get('calories') or 0

        # Sort by date
        sorted_dates = sorted(date_totals.keys())
        if not sorted_dates:
            return None

        # Create a simple ASCII chart
        max_calories = max(date_totals.values()) if date_totals else 0
        chart_lines = ["Daily Calorie Intake (Last {} days):".format(days)]

        for date in sorted_dates[-min(days, len(sorted_dates)):]:  # Last N days
            calories = date_totals[date]
            bar_length = int((calories / max(max_calories, 1)) * 20)  # Scale to 20 chars
            bar = "█" * bar_length
            chart_lines.append(f"{date}: {bar} ({calories} cal)")

        return "\n".join(chart_lines)
    except Exception as e:
        print(f"Error generating nutrition chart: {e}")
        return None

def generate_goal_progress_chart(user, days=30):
    """Generate goal progress chart - simplified version without matplotlib"""
    try:
        goal = UserGoal.objects.get(user=user)
    except UserGoal.DoesNotExist:
        return None

    activities, nutrition = get_user_data(user, days)

    # Calculate progress
    dates = []
    burned_progress = []
    consumed_progress = []
    protein_progress = []

    end_date = datetime.now().date()
    for i in range(days):
        date = end_date - timedelta(days=i)
        dates.append(date)

        # Activity progress
        day_activities = [a for a in activities if a['date'] == date]
        burned = sum(a.get('calories_burned', 0) for a in day_activities) if day_activities else 0
        burned_progress.append(burned / goal.target_calories_burn if goal.target_calories_burn > 0 else 0)

        # Nutrition progress
        day_nutrition = [n for n in nutrition if n['date'] == date]
        consumed = sum(n.get('calories', 0) for n in day_nutrition) if day_nutrition else 0
        consumed_progress.append(consumed / goal.target_calories_consume if goal.target_calories_consume > 0 else 0)

        protein = sum(n.get('protein', 0) for n in day_nutrition) if day_nutrition else 0
        protein_progress.append(protein / goal.target_protein if goal.target_protein > 0 else 0)

    dates.reverse()
    burned_progress.reverse()
    consumed_progress.reverse()
    protein_progress.reverse()

    # Create a simple text-based progress report
    try:
        chart_lines = ["Goal Progress Summary (Last {} days):".format(days)]
        chart_lines.append("")

        # Calculate averages
        avg_burned_progress = sum(burned_progress) / len(burned_progress) if burned_progress else 0
        avg_consumed_progress = sum(consumed_progress) / len(consumed_progress) if consumed_progress else 0
        avg_protein_progress = sum(protein_progress) / len(protein_progress) if protein_progress else 0

        chart_lines.append(f"Calories Burned: {avg_burned_progress:.2f} (Target: {goal.target_calories_burn})")
        chart_lines.append(f"Calorie Intake: {avg_consumed_progress:.2f} (Target: {goal.target_calories_consume})")
        chart_lines.append(f"Protein Intake: {avg_protein_progress:.2f} (Target: {goal.target_protein})")
        chart_lines.append("")

        # Progress indicators
        chart_lines.append("Progress Indicators:")
        chart_lines.append(f"Burned: {'✓' if avg_burned_progress >= 0.8 else '⚠' if avg_burned_progress >= 0.5 else '✗'}")
        chart_lines.append(f"Consumed: {'✓' if avg_consumed_progress <= 1.2 else '⚠' if avg_consumed_progress <= 1.5 else '✗'}")
        chart_lines.append(f"Protein: {'✓' if avg_protein_progress >= 0.8 else '⚠' if avg_protein_progress >= 0.5 else '✗'}")

        return "\n".join(chart_lines)
    except Exception as e:
        print(f"Error generating goal progress chart: {e}")
        return None

def generate_recommendations(user, trends, goal=None):
    """Generate personalized recommendations based on data analysis"""
    recommendations = []

    if goal:
        # Goal-based recommendations
        if goal.goal_type == 'weight_loss':
            if trends['avg_daily_calories_consumed'] > goal.target_calories_consume:
                recommendations.append({
                    'type': 'warning',
                    'title': 'Calorie Intake Too High',
                    'message': f'Your average daily calorie intake ({trends["avg_daily_calories_consumed"]}) exceeds your target ({goal.target_calories_consume}). Consider reducing portion sizes.',
                    'action': 'Reduce daily calories by 200-300 to support weight loss.'
                })
            if trends['avg_activity_days'] < goal.target_activity_days:
                recommendations.append({
                    'type': 'info',
                    'title': 'Increase Activity Frequency',
                    'message': f'Your current activity frequency ({trends["avg_activity_days"]} days/week) is below your target ({goal.target_activity_days} days/week).',
                    'action': 'Try to be active at least 3-4 days per week.'
                })

        elif goal.goal_type == 'muscle_gain':
            if trends['avg_daily_protein'] < goal.target_protein:
                recommendations.append({
                    'type': 'info',
                    'title': 'Increase Protein Intake',
                    'message': f'Your protein intake ({trends["avg_daily_protein"]}g) is below the recommended target ({goal.target_protein}g) for muscle gain.',
                    'action': 'Include more protein-rich foods like chicken, fish, eggs, and legumes.'
                })

        elif goal.goal_type == 'increase_fitness':
            if trends['trend_calories_burned'] <= 0:
                recommendations.append({
                    'type': 'warning',
                    'title': 'Activity Level Declining',
                    'message': 'Your calorie burn trend is not improving. Consider increasing workout intensity or duration.',
                    'action': 'Try adding 10-15 minutes to your workouts or increasing intensity.'
                })

    # General recommendations based on trends
    if trends['avg_daily_calories_burned'] < 500:
        recommendations.append({
            'type': 'info',
            'title': 'Low Activity Level',
            'message': f'Your average daily calorie burn ({trends["avg_daily_calories_burned"]}) is quite low.',
            'action': 'Aim for at least 30 minutes of moderate activity daily.'
        })

    if trends['trend_calories_consumed'] > 50:  # Increasing trend
        recommendations.append({
            'type': 'warning',
            'title': 'Rising Calorie Intake',
            'message': 'Your calorie consumption is trending upward. Monitor portion sizes.',
            'action': 'Track your meals more carefully and consider smaller portions.'
        })

    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Great Progress!',
            'message': 'Your health metrics look good. Keep up the excellent work!',
            'action': 'Continue your current healthy habits.'
        })

    return recommendations
    """Get user's activity and nutrition data for the last N days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    activities = Activity.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'duration', 'calories_burned', 'distance')

    nutrition = NutritionEntry.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'calories', 'protein', 'carbs', 'fat')

    return list(activities), list(nutrition)

def calculate_trends(activities, nutrition, days=30):
    """Calculate trends and averages using basic Python operations"""
    if not activities and not nutrition:
        return {
            'avg_daily_calories_burned': 0,
            'avg_daily_calories_consumed': 0,
            'avg_daily_protein': 0,
            'avg_activity_days': 0,
            'trend_calories_burned': 0,
            'trend_calories_consumed': 0,
        }

    # Calculate basic averages
    total_burned = sum(a.get('calories_burned') or 0 for a in activities)
    total_consumed = sum(n.get('calories') or 0 for n in nutrition)
    total_protein = sum(n.get('protein') or 0 for n in nutrition)

    avg_daily_calories_burned = total_burned / days if activities else 0
    avg_daily_calories_consumed = total_consumed / days if nutrition else 0
    avg_daily_protein = total_protein / days if nutrition else 0

    # Calculate activity days (unique dates with activity)
    activity_dates = set()
    for activity in activities:
        if activity.get('duration', 0) > 0:
            activity_dates.add(activity['date'])
    avg_activity_days = len(activity_dates) / (days / 7)  # per week

    # Simple trend calculation (comparing first half vs second half)
    mid_point = days // 2

    # For activities trend
    first_half_activities = []
    second_half_activities = []

    for activity in activities:
        days_since = (datetime.now().date() - activity['date']).days
        if days_since >= mid_point:
            first_half_activities.append(activity)
        else:
            second_half_activities.append(activity)

    first_half_burned = sum(a.get('calories_burned') or 0 for a in first_half_activities)
    second_half_burned = sum(a.get('calories_burned') or 0 for a in second_half_activities)

    total_activities_count = len(first_half_activities) + len(second_half_activities)
    trend_calories_burned = (second_half_burned - first_half_burned) / max(1, total_activities_count)

    # For nutrition trend
    first_half_nutrition = []
    second_half_nutrition = []

    for entry in nutrition:
        days_since = (datetime.now().date() - entry['date']).days
        if days_since >= mid_point:
            first_half_nutrition.append(entry)
        else:
            second_half_nutrition.append(entry)

    first_half_consumed = sum(n.get('calories') or 0 for n in first_half_nutrition)
    second_half_consumed = sum(n.get('calories') or 0 for n in second_half_nutrition)

    total_nutrition_count = len(first_half_nutrition) + len(second_half_nutrition)
    trend_calories_consumed = (second_half_consumed - first_half_consumed) / max(1, total_nutrition_count)

    return {
        'avg_daily_calories_burned': round(avg_daily_calories_burned, 1),
        'avg_daily_calories_consumed': round(avg_daily_calories_consumed, 1),
        'avg_daily_protein': round(avg_daily_protein, 1),
        'avg_activity_days': round(avg_activity_days, 1),
        'trend_calories_burned': round(trend_calories_burned, 2),
        'trend_calories_consumed': round(trend_calories_consumed, 2),
    }

def calculate_trend(series):
    """Calculate linear trend slope"""
    if len(series) < 2:
        return 0

    if not NUMPY_AVAILABLE:
        # Simple trend calculation without numpy/sklearn
        if len(series) >= 2:
            first_half = sum(series[:len(series)//2]) / max(1, len(series)//2)
            second_half = sum(series[len(series)//2:]) / max(1, len(series) - len(series)//2)
            return second_half - first_half
        return 0

    if np.std(series) == 0:  # No variation
        return 0

    model = LinearRegression()
    model.fit(X, y)
    return model.coef_[0]

def generate_goal_progress_chart(user, days=30):
    """Generate goal progress chart"""
    try:
        goal = UserGoal.objects.get(user=user)
    except UserGoal.DoesNotExist:
        return None

    activities, nutrition = get_user_data(user, days)

    # Calculate progress
    dates = []
    burned_progress = []
    consumed_progress = []
    protein_progress = []

    end_date = datetime.now().date()
    for i in range(days):
        date = end_date - timedelta(days=i)
        dates.append(date)

        # Activity progress
        day_activities = [a for a in activities if a['date'] == date]
        burned = sum(a.get('calories_burned', 0) for a in day_activities) if day_activities else 0
        burned_progress.append(burned / goal.target_calories_burn if goal.target_calories_burn > 0 else 0)

        # Nutrition progress
        day_nutrition = [n for n in nutrition if n['date'] == date]
        consumed = sum(n.get('calories', 0) for n in day_nutrition) if day_nutrition else 0
        consumed_progress.append(consumed / goal.target_calories_consume if goal.target_calories_consume > 0 else 0)

        protein = sum(n.get('protein', 0) for n in day_nutrition) if day_nutrition else 0
        protein_progress.append(protein / goal.target_protein if goal.target_protein > 0 else 0)

    dates.reverse()
    burned_progress.reverse()
    consumed_progress.reverse()
    protein_progress.reverse()

    # Create a simple text-based progress report
    try:
        chart_lines = ["Goal Progress Summary (Last {} days):".format(days)]
        chart_lines.append("")

        # Calculate averages
        avg_burned_progress = sum(burned_progress) / len(burned_progress) if burned_progress else 0
        avg_consumed_progress = sum(consumed_progress) / len(consumed_progress) if consumed_progress else 0
        avg_protein_progress = sum(protein_progress) / len(protein_progress) if protein_progress else 0

        chart_lines.append(f"Calories Burned: {avg_burned_progress:.2f} (Target: {goal.target_calories_burn})")
        chart_lines.append(f"Calorie Intake: {avg_consumed_progress:.2f} (Target: {goal.target_calories_consume})")
        chart_lines.append(f"Protein Intake: {avg_protein_progress:.2f} (Target: {goal.target_protein})")
        chart_lines.append("")

        # Progress indicators
        chart_lines.append("Progress Indicators:")
        chart_lines.append(f"Burned: {'✓' if avg_burned_progress >= 0.8 else '⚠' if avg_burned_progress >= 0.5 else '✗'}")
        chart_lines.append(f"Consumed: {'✓' if avg_consumed_progress <= 1.2 else '⚠' if avg_consumed_progress <= 1.5 else '✗'}")
        chart_lines.append(f"Protein: {'✓' if avg_protein_progress >= 0.8 else '⚠' if avg_protein_progress >= 0.5 else '✗'}")

        return "\n".join(chart_lines)
    except Exception as e:
        print(f"Error generating goal progress chart: {e}")
        return None

def generate_recommendations(user, trends, goal=None):
    """Generate personalized recommendations based on data analysis"""
    recommendations = []

    if goal:
        # Goal-based recommendations
        if goal.goal_type == 'weight_loss':
            if trends['avg_daily_calories_consumed'] > goal.target_calories_consume:
                recommendations.append({
                    'type': 'warning',
                    'title': 'Calorie Intake Too High',
                    'message': f'Your average daily calorie intake ({trends["avg_daily_calories_consumed"]}) exceeds your target ({goal.target_calories_consume}). Consider reducing portion sizes.',
                    'action': 'Reduce daily calories by 200-300 to support weight loss.'
                })
            if trends['avg_activity_days'] < goal.target_activity_days:
                recommendations.append({
                    'type': 'info',
                    'title': 'Increase Activity Frequency',
                    'message': f'Your current activity frequency ({trends["avg_activity_days"]} days/week) is below your target ({goal.target_activity_days} days/week).',
                    'action': 'Try to be active at least 3-4 days per week.'
                })

        elif goal.goal_type == 'muscle_gain':
            if trends['avg_daily_protein'] < goal.target_protein:
                recommendations.append({
                    'type': 'info',
                    'title': 'Increase Protein Intake',
                    'message': f'Your protein intake ({trends["avg_daily_protein"]}g) is below the recommended target ({goal.target_protein}g) for muscle gain.',
                    'action': 'Include more protein-rich foods like chicken, fish, eggs, and legumes.'
                })

        elif goal.goal_type == 'increase_fitness':
            if trends['trend_calories_burned'] <= 0:
                recommendations.append({
                    'type': 'warning',
                    'title': 'Activity Level Declining',
                    'message': 'Your calorie burn trend is not improving. Consider increasing workout intensity or duration.',
                    'action': 'Try adding 10-15 minutes to your workouts or increasing intensity.'
                })

    # General recommendations based on trends
    if trends['avg_daily_calories_burned'] < 500:
        recommendations.append({
            'type': 'info',
            'title': 'Low Activity Level',
            'message': f'Your average daily calorie burn ({trends["avg_daily_calories_burned"]}) is quite low.',
            'action': 'Aim for at least 30 minutes of moderate activity daily.'
        })

    if trends['trend_calories_consumed'] > 50:  # Increasing trend
        recommendations.append({
            'type': 'warning',
            'title': 'Rising Calorie Intake',
            'message': 'Your calorie consumption is trending upward. Monitor portion sizes.',
            'action': 'Track your meals more carefully and consider smaller portions.'
        })

    if not recommendations:
        recommendations.append({
            'type': 'success',
            'title': 'Great Progress!',
            'message': 'Your health metrics look good. Keep up the excellent work!',
            'action': 'Continue your current healthy habits.'
        })

    return recommendations