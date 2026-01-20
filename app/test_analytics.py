import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

# Test the exact function that's failing
from health.analytics import generate_nutrition_chart, get_user_data
from django.contrib.auth.models import User

try:
    user = User.objects.get(username='testuser')
    activities, nutrition = get_user_data(user, 90)
    chart = generate_nutrition_chart(nutrition, 90)
    print('SUCCESS: generate_nutrition_chart worked!')
    print('Chart type:', type(chart))
    print('Chart length:', len(chart) if chart else 0)
except Exception as e:
    print('ERROR:', e)
    import traceback
    traceback.print_exc()