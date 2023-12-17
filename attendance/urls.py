from django.contrib import admin
from django.urls import path, include
from . import views
from .thread import ClockThread


urlpatterns = [
    path("", views.home, name="home"),
    path("all_records", views.all_records, name="all_records"),
    path("load_to_db", views.load_employee_data_to_db, name="load_to_db"),
    path("clock_in", views.clock_in, name="clock_in"),
    path("clock_out", views.clock_out, name="clock_out"),
    path("employees", views.employees, name="employees")
]
