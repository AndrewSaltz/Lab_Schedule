import datetime
from datetime import date
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labschedule.settings")
django.setup()
from schedule.models import Event, period_choices, cart_choice


def run():
        to_monday = date.today().weekday()
        start = date.today() - datetime.timedelta(days=to_monday) #Find Monday
        day = start # Day will change, start will not
        end = start + datetime.timedelta(days=7)  # One week, edit later for flexibility
        weekend = set([5, 6])  # Python week starts on Monday as 0
        total = 0
        while start <= end:
            if start.weekday() not in weekend:
                for period in period_choices:
                    for cart in cart_choice:
                        open = Event(day=day, period=period[0], cart=cart[0])
                        print(open)
                        total+=1
                start += datetime.timedelta(days=1)  # Adds one day until the current day is past the end day
                print(day)