import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labschedule.settings")
django.setup()
import datetime
from datetime import date
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from labschedule import settings
from schedule.models import Event, cart_choice

# Mostly use this to test whether or not I can send emails

def run():
    today = date.today()
    subject = "Daily Report for %s" % today
    to = [settings.EMAIL_ADMIN]
    from_email = 'andrewsaltz@gmail.com' # My email

    reservations = Event.objects.filter(day=today).order_by('cart')
    last = Event.objects.latest('day')
    if today >= today + datetime.timedelta(days=5):
        countdown = last - datetime.timedelta(today)
        warning = "Hey! You run out of open slots in %s days" % countdown
    else:
        warning = None

    ctx = ({
        'reservations' : reservations, 'warning' : warning, 'cart_choice' : cart_choice
    })
    html_content = render_to_string('schedule/email.html', ctx)
    text_content = render_to_string('schedule/email.html', ctx)
    msg = EmailMultiAlternatives(subject, text_content, to=to, from_email=from_email)
    msg.attach_alternative(html_content, "text/html")
    weekend = set([5, 6])  # Python week starts on Monday as 0
    if today.weekday() not in weekend and settings.DAILY_EMAIL == True:
        msg.send()
        print ('Email sent!')
    else:
        pass