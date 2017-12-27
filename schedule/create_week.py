import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labschedule.settings")
django.setup()

from schedule.models import Event

days = ('Monday', 'Tuesday',)
# Add the rest later

for day in days:
    for period in period_choices:
        for cart in cart_choice:
            print(day, cart, period)

print("All done!")
