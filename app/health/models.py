from django.db import models
# from django.contrib.auth.models import User


class UserGoal(models.Model):
    GOAL_TYPES = [
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintain_weight', 'Maintain Weight'),
        ('increase_fitness', 'Increase Fitness'),
        ('improve_endurance', 'Improve Endurance'),
    ]

    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    goal_type = models.CharField(
        max_length=50,
        choices=GOAL_TYPES,
        default='maintain_weight'
    )
    target_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Target weight in kg"
    )
    target_calories_burn = models.PositiveIntegerField(
        default=2000,
        help_text="Daily calories to burn"
    )
    target_calories_consume = models.PositiveIntegerField(
        default=2000,
        help_text="Daily calories to consume"
    )
    target_protein = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        help_text="Daily protein target in grams"
    )
    target_activity_days = models.PositiveIntegerField(
        default=3,
        help_text="Days per week for activity"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.user.username}'s {self.get_goal_type_display()} goal"

    def __str__(self):
        return f"{self.get_goal_type_display()} goal"

class Activity(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    activity_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )
    distance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance in km"
    )
    calories_burned = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.activity_type} on {self.date}"


class NutritionEntry(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    food_name = models.CharField(max_length=200)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Protein in grams"
    )
    carbs = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Carbs in grams"
    )
    fat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fat in grams"
    )
    quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Quantity in grams or servings"
    )
    date = models.DateField()
    meal_type = models.CharField(
        max_length=50,
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
        ]
    )

    def __str__(self):
        return f"{self.food_name} on {self.date}"
