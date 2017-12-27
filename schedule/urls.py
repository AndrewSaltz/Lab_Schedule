from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^week/(?P<adjuster>\d+)/$', views.Home.as_view(template_name="schedule/home.html"), name='home'),
    url(r'^reserve/$', views.reserve, name='reserve'),
    url(r'^dashboard/$', views.Dashboard.as_view(template_name="schedule/dashboard.html"), name='dashboard'),
    url(r'^create_week/$', views.create_week, name='create_week'),
    url(r'^create_month/$', views.create_month, name='create_month'),
    url(r'^create_twelve/$', views.create_twelve, name='create_twelve'),
    url(r'^delete_all/$', views.delete_all, name="delete_all"),
    url('^login/$', auth_views.LoginView.as_view(), name="login"),
    url('^logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^$', views.redirect_root)
    ]
