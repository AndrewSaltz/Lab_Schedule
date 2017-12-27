from django import template
from datetime import datetime
from django.utils.dateparse import parse_date

register = template.Library()

@register.filter
def the_day(value):
    answer = parse_date(value)
    return answer.weekday()

@register.filter
def back_day(value):
    value = value.strip( )
    if int(value) > 0:
        answer = int(value) - 1
        return answer
    else:
        answer = int(value)
        return answer