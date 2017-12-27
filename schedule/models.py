from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from recurrence.fields import RecurrenceField

# Set the Periods. Two entry tuple (). Our Third period is adivisory
period_choices = (
    (1, 1),
    (2, 2),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
)
# Set your carts. We have 4 carts and a lab
cart_choice = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('LAB', 'LAB')
)


# Create your models here.
class Event(models.Model):
    day = models.DateField(blank=False, null=False)
    period = models.IntegerField(choices=period_choices)
    cart = models.CharField(choices=cart_choice, max_length=4)
    is_reserved = models.BooleanField(default=False)
    teacher = models.ForeignKey(User, blank=True, null=True)
    # recurrences = RecurrenceField()  # I don't think we need this

    class Meta:
        unique_together = ('day', 'period', 'cart')

    def __str__(self):
        return "%s on %s period %s, cart %s" % (self.is_reserved, self.day, self.period, self.cart)
