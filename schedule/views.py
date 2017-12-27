from django.shortcuts import render
import datetime
from datetime import date
import calendar
from schedule.models import Event, period_choices, cart_choice
from django.views.generic import UpdateView, TemplateView, ListView
from schedule.forms import ReservationForm
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
import json
import calendar
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User




class Home(LoginRequiredMixin, ListView):
    model = Event
    template_name = "schedule/home.html"
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        q = self.kwargs['adjuster'] #Change week
        adjust = int(q)
        if adjust != 0:
            adjust *=7 # Add to Monday to move up and down weeks
        today = date.today()
        Monday = date.today() - datetime.timedelta(days=date.today().weekday())
        Friday = Monday + datetime.timedelta(days=4)
        Monday = Monday + datetime.timedelta(days=adjust)
        Friday = Friday + datetime.timedelta(days=adjust) # Alter the days if needed. Really non-pythony
        context['monday'] = Monday
        context['q'] = q
        context['this_week'] = Event.objects.filter(day__gte=Monday,day__lte=Friday)
        context['the_day'] = calendar.day_name[today.weekday()]
        periods = []
        user = self.request.user
        context['my_reservation'] = Event.objects.filter(day__gte=Monday,day__lte=Friday,teacher=user.id)
        for p in period_choices:
            periods.append(p[1])
        context['periods'] = periods
        context['username'] = self.request.user.username
        return context

@ensure_csrf_cookie
def reserve(request):
    if request.is_ajax():
        pk = request.POST['pk']
        slot = Event.objects.get(pk=pk)
        user = request.user
        if slot.is_reserved == True:
            if user == slot.teacher:
                slot.is_reserved = False
                slot.teacher = None
                slot.save()
                result = 1
            elif user.is_superuser and user != slot.teacher: # Override as admin
                slot.is_reserved == True
                slot.teacher = user
                slot.save()
                result = 2
            else:
                result = 3
        else:
            slot.is_reserved = True
            slot.teacher = user
            slot.save()
            result = 2
    data = {'result': result}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

class Dashboard(PermissionRequiredMixin,TemplateView):
    template_name = "schedule/dashboard.html"
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        periods = []
        for p in period_choices:
            periods.append(p[1])
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        cart_list =[]
        for cart in cart_choice:
            cart_list.append(cart[0])
        context['periods']=periods # Make this a mixin
        context['this_day'] = Event.objects.filter(day=today)
        context['next_day'] = Event.objects.filter(day=tomorrow)
        context['cart_list'] = cart_list
        context['today'] = today
        context['tomorrow'] = tomorrow
        return context

@ensure_csrf_cookie
def create_week(request):
    if request.is_ajax():
        to_monday = date.today().weekday()
        start = date.today() - datetime.timedelta(days=to_monday) #Find Monday
        day = start # Day will change, start will not
        end = start + datetime.timedelta(days=4)  # One week, edit later for flexibility
        weekend = set([5, 6])  # Python week starts on Monday as 0
        dupe_list = []
        total = 0
        while day <= end:
                if day.weekday() not in weekend:
                    for period in period_choices:
                        for cart in cart_choice:
                            open = Event(day=day, period=period[0], cart=cart[0])
                            try:
                                open.save()
                                total+=1
                            except IntegrityError:
                                dupe = str(open)
                                dupe_list.append(dupe)
                                pass
                day += datetime.timedelta(days=1)  # Adds one day until the current day is past the end day
        data = {'start': start, 'end': end, 'dupe_list': dupe_list, 'total': total}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))


def redirect_root(request):
    return HttpResponseRedirect('/week/0/')

@ensure_csrf_cookie
def create_month(request):
    if request.is_ajax():
        month = date.today().month
        year = date.today().year
       # last = calendar.monthrange(year, month) # Last day
        start = date.today().replace(day=1) # Get the first day of the month
        end = date.today().replace(day=(calendar.monthrange(year, month)[1]))
        weekend = set([5, 6])  # Python week starts on Monday as 0
        dupe_list = []
        total = 0
        day = start
        while day <= end:
            if day.weekday() not in weekend:
                    for period in period_choices:
                        for cart in cart_choice:
                            open = Event(day=day, period=period[0], cart=cart[0])
                            try:
                                open.save()
                                total+=1
                            except IntegrityError:
                                dupe = str(open)
                                dupe_list.append(dupe)
                                pass
            day += datetime.timedelta(days=1)
        data = {'start': start, 'end': end, 'dupe_list': dupe_list, 'total': total}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

@ensure_csrf_cookie
def create_twelve(request):
    if request.is_ajax():
        to_monday = date.today().weekday()
        start = date.today() - datetime.timedelta(days=to_monday)  # Find Monday
        fake_end = start + datetime.timedelta(days=84)
        if fake_end.weekday() != 4:
            end = fake_end - datetime.timedelta(days=(fake_end.weekday() - 4))
        else:
            end = fake_end
        day = start
        total = 0
        dupe_list = []
        weekend = set([5, 6])  # Python week starts on Monday as 0
        while day <= end:
            if day.weekday() not in weekend:
                    for period in period_choices:
                        for cart in cart_choice:
                            open = Event(day=day, period=period[0], cart=cart[0])
                            try:
                                open.save()
                                total+=1
                            except IntegrityError:
                                dupe = str(open)
                                dupe_list.append(dupe)
                                pass
            day += datetime.timedelta(days=1)
        data = {'start': start, 'end': end, 'dupe_list': dupe_list, 'total': total}
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder))

@ensure_csrf_cookie
def delete_all(request):
    if request.is_ajax():
        Event.objects.all().delete()
    return HttpResponse()

