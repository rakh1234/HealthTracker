from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Activity, NutritionEntry, UserGoal
from .forms import ActivityForm, NutritionEntryForm, UserGoalForm


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'health/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'health/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'health/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    # Get today's date
    today = timezone.now().date()

    # Get recent activities (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_activities = Activity.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')[:10]

    # Get recent nutrition entries (last 7 days)
    recent_nutrition = NutritionEntry.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')[:10]

    # Calculate today's totals
    today_activities = Activity.objects.filter(
        user=request.user, date=today
    )
    today_calories_burned = today_activities.aggregate(
        Sum('calories_burned')
    )['calories_burned__sum'] or 0
    today_duration = today_activities.aggregate(
        Sum('duration')
    )['duration__sum'] or 0

    today_nutrition = NutritionEntry.objects.filter(
        user=request.user, date=today
    )
    today_calories_consumed = today_nutrition.aggregate(
        Sum('calories')
    )['calories__sum'] or 0
    today_protein = today_nutrition.aggregate(
        Sum('protein')
    )['protein__sum'] or 0
    today_carbs = today_nutrition.aggregate(
        Sum('carbs')
    )['carbs__sum'] or 0
    today_fat = today_nutrition.aggregate(
        Sum('fat')
    )['fat__sum'] or 0

    # Get user goal
    try:
        user_goal = UserGoal.objects.get(user=request.user)
    except UserGoal.DoesNotExist:
        user_goal = None

    context = {
        'recent_activities': recent_activities,
        'recent_nutrition': recent_nutrition,
        'today_calories_burned': today_calories_burned,
        'today_duration': today_duration,
        'today_calories_consumed': today_calories_consumed,
        'today_protein': today_protein,
        'today_carbs': today_carbs,
        'today_fat': today_fat,
        'user_goal': user_goal,
    }
    return render(request, 'health/dashboard.html', context)


@login_required
def goal_settings(request):
    """Manage user goals"""
    try:
        goal = UserGoal.objects.get(user=request.user)
    except UserGoal.DoesNotExist:
        goal = None

    if request.method == 'POST':
        if goal:
            form = UserGoalForm(request.POST, instance=goal)
        else:
            form = UserGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Your goals have been updated successfully!')
            return redirect('dashboard')
    else:
        if goal:
            form = UserGoalForm(instance=goal)
        else:
            form = UserGoalForm()

    return render(
        request,
        'health/goal_settings.html',
        {'form': form, 'goal': goal}
    )


@login_required
def activity_list(request):
    activities = Activity.objects.filter(
        user=request.user
    ).order_by('-date')
    return render(
        request,
        'health/activity_list.html',
        {'activities': activities}
    )


@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity logged successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(
        request,
        'health/activity_form.html',
        {'form': form, 'title': 'Log Activity'}
    )


@login_required
def activity_update(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(
        request,
        'health/activity_form.html',
        {'form': form, 'title': 'Update Activity'}
    )


@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_list')
    return render(
        request,
        'health/activity_confirm_delete.html',
        {'activity': activity}
    )


@login_required
def nutrition_list(request):
    nutrition_entries = NutritionEntry.objects.filter(
        user=request.user
    ).order_by('-date')
    return render(
        request,
        'health/nutrition_list.html',
        {'nutrition_entries': nutrition_entries}
    )

@login_required
def nutrition_create(request):
    if request.method == 'POST':
        form = NutritionEntryForm(request.POST)
        if form.is_valid():
            nutrition = form.save(commit=False)
            nutrition.user = request.user
            nutrition.save()
            messages.success(request, 'Nutrition entry logged successfully!')
            return redirect('nutrition_list')
    else:
        form = NutritionEntryForm()
    return render(
        request,
        'health/nutrition_form.html',
        {'form': form, 'title': 'Log Nutrition'}
    )

@login_required
def nutrition_update(request, pk):
    nutrition = get_object_or_404(NutritionEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NutritionEntryForm(request.POST, instance=nutrition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nutrition entry updated successfully!')
            return redirect('nutrition_list')
    else:
        form = NutritionEntryForm(instance=nutrition)
    return render(
        request,
        'health/nutrition_form.html',
        {'form': form, 'title': 'Update Nutrition'}
    )


@login_required
def nutrition_delete(request, pk):
    nutrition = get_object_or_404(NutritionEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        nutrition.delete()
        messages.success(request, 'Nutrition entry deleted successfully!')
        return redirect('nutrition_list')
    return render(
        request,
        'health/nutrition_confirm_delete.html',
        {'nutrition': nutrition}
    )
