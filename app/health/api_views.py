from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Activity, NutritionEntry, UserGoal
from .serializers import (
    ActivitySerializer,
    NutritionEntrySerializer,
    UserGoalSerializer
)


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NutritionEntryViewSet(viewsets.ModelViewSet):
    serializer_class = NutritionEntrySerializer
    permission_classes = [IsAuthenticated]
    queryset = NutritionEntry.objects.all()

    def get_queryset(self):
        return NutritionEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserGoalViewSet(viewsets.ModelViewSet):
    serializer_class = UserGoalSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserGoal.objects.all()

    def get_queryset(self):
        return UserGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure only one goal per user
        UserGoal.objects.filter(user=self.request.user).delete()
        serializer.save(user=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the current user"""
    today = timezone.now().date()

    # Today's totals
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

    # Recent activities (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_activities = Activity.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')[:5]

    # Recent nutrition (last 7 days)
    recent_nutrition = NutritionEntry.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')[:5]

    # User goal
    try:
        user_goal = UserGoal.objects.get(user=request.user)
        goal_data = UserGoalSerializer(user_goal).data
    except UserGoal.DoesNotExist:
        goal_data = None

    return Response({
        'today_stats': {
            'calories_burned': today_calories_burned,
            'duration': today_duration,
            'calories_consumed': today_calories_consumed,
            'protein': today_protein,
            'carbs': today_carbs,
            'fat': today_fat,
        },
        'recent_activities': ActivitySerializer(
            recent_activities, many=True
        ).data,
        'recent_nutrition': NutritionEntrySerializer(
            recent_nutrition, many=True
        ).data,
        'user_goal': goal_data,
    })