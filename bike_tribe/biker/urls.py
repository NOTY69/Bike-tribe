from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.login_user,name="login"),
    path("register/",views.register_user,name="register"),
    path("home/",views.home,name="home"),
    path("profile/",views.profile_update,name="profile"),
    path("bike_info/<int:distance>",views.bike_info,name="bike_info"),
    path("create/",views.create,name="create"),
    path("leaderboard/",views.leaderboard,name="leaderboard"),
    path("message/<int:travel_id>",views.message,name="message"),
    path("milage/",views.milage,name="petrol_expense_calculator"),
    path('join_travel/', views.join_travel, name='join'),
    path("view_notes/<int:notes_id>",views.see_notes,name="view_notes"),
    path("my_travel/",views.my_t,name="my_t"),
]
