from django.test import TestCase
from django.utils import timezone
import datetime
from datetime import date
from schedule.models import Event, period_choices, cart_choice
from django.contrib.auth.models import User
from django.test import Client

# Create your tests here.

from schedule.models import Event

class EventTest(TestCase):
    # Done before adding reoccurence

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')


    def tearDown(self):
        self.user.delete()

    def test_event(self):
        object = Event.objects.create(day=date.today(), period=1, cart=1, teacher=self.user, is_reserved = True)
        self.assertTrue(object.day == date.today())
        self.assertTrue(object.teacher == self.user)
        self.assertTrue(object.period == 1)
        self.assertTrue(object.cart == 1)
        self.assertTrue(object.is_reserved == True)

class Create_Week_Test(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)

    def tearDown(self):
        self.user.delete()

    def test_create_week(self):
        c = Client()

        response = c.post('/create_week/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, "create_week failed")

class Create_Month_Test(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)

    def tearDown(self):
        self.user.delete()

    def test_create_week(self):
        c = Client()
        response = c.post('/create_month/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, "create_month failed")

class Create_Twelve_Test(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)

    def tearDown(self):
        self.user.delete()

    def test_create_week(self):
        c = Client()
        response = c.post('/create_twelve/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, "create_long failed")


class Reservation_Test(TestCase):

    def setUp(self):
        self.object = Event.objects.create(pk=1, day=date.today(), period=1, cart=1, teacher=None, is_reserved = False)
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)

    def tearDown(self):
        self.user.delete()

    def reservation_test(self):
        c = Client()

        response = c.post('/reserve/', {'pk' : 1, 'user' : user, 'cart' : 1, 'date' : date.today()})
        #self.assertEqual(response.status_code, 200, "create_reservation failed")
        self.assertTrue(response, self.object.is_reserved == True)

# class Double_Book_Test(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='12345', is_staff=True)
#         self.user_two = User.objects.create_user(username="testtwo", password='678910')
#
#     def tearDown(self):
#         self.user.delete()
#
#     def double_test(self):
#         self.object = Event.objects.create(day=date.today(), period=1, cart=1, teacher=self.user, is_reserved = True)
#         self assertTrue

class Test_Admin(TestCase):

    def setUp(self):
        self.object = Event.objects.create(pk=1, day=date.today(), period=1, cart=1, teacher=None, is_reserved = False)
        self.user = User.objects.create_user(username='testuser', password='12345', is_staff=False)
        self.admin = User.objects.create_user(username='boss', password='678910', is_superuser=True)

    def tearDown(self):
        self.user.delete()
        self.boss.delete()
        self.object.delete

    def first_test(self):
        c = Client()
        boss = self.admin
        user = self.user
        response = c.post('/reserve/', {'pk': 1, 'user': user, 'cart': 1, 'date': date.today()})
        self.assertTrue(response, self.object.is_reserved == True)
        next = c.post('/reserve/', {'pk' : 1, 'user': boss, })
        self.assertTrue(next, self.object.teacher == boss)