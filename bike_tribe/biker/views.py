from django.shortcuts import render
from .models import travel_plan
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import connection
from django.contrib.auth.hashers import make_password
import json
# Create your views here.
def login_user(request):
#    models.travel_plan.objects.all().delete()

# # Step 2: Reset auto-increment counter
#    with connection.cursor() as cursor:
#       cursor.execute("ALTER TABLE biker_travel_plan AUTO_INCREMENT = 1;")
   if request.method=="POST":
      username=request.POST.get('username')
      password=request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         messages.success(request, "Logged in successfully.")
         return redirect("home") 
      else:
            messages.error(request, "Invalid username or password")
            return render(request, "biker/login.html")
   return render(request,"biker\login.html")
def register_user(request):
   if request.method == 'POST':
      username=request.POST.get('username')
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      email = request.POST.get('email')
      password = request.POST.get('password')
      confirm_password = request.POST.get('confirm_password')

      if password != confirm_password:
         messages.error(request, "Passwords do not match.")
         return render(request, 'docs/register.html')

      if User.objects.filter(username=email).exists():
         messages.error(request, "User with this email already exists.")
         return render(request, 'docs/register.html')

      user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
         )
      user.save()
      models.Points.objects.create(user=user, points=0)
      messages.success(request, "Registration successful! Please login.")
      return redirect('login') 
   return render(request,"biker/register.html")
def home(request):
   if request.method=="POST":
      travel_id=request.data.get("id")
      current_user=User.objects.get(request.user.username)
      plan=models.travel_plan.objects.get(pk=travel_id)

      if models.Joined_Members.objects.filter(user=current_user,travelplan=plan).exists():
         return redirect("home")
      models.Joined_Members.objects.create(user=current_user,travelplan=plan)
      return redirect("home")
   
   travels=models.travel_plan.objects.all()
   current_user=User.objects.get(username=request.user.username)
   user_joined_trips=models.Joined_Members.objects.filter(user=current_user)

   return render(request,"biker/home.html",{"travels":travels,"user_joined_trips":user_joined_trips})
def profile_update(request):
   return render(request,"biker/profile.html")
def bike_info(request,distance):
   if request.method=="POST":
      bike_name=request.POST.get("bikeName")
      cc=request.POST.get("cc")
      km=request.POST.get("distance")

      models.bike_info.objects.create(
         bike_name=bike_name,
         cc=cc,
         km=km,
      )
      return redirect("petrol_expense_calculator")
   return render(request,"biker/bike_info.html",{"distance":distance})
def create(request):
   user=request.user
   if request.method=="POST":
      host=request.POST.get("host")
      starting_point=request.POST.get("startingPoint")
      ending_point=request.POST.get("endingPoint")
      date_range=request.POST.get("dateRange")
      start_time=request.POST.get("starttime")
      km=request.POST.get("kilometers")
      number_of_persons = request.POST.get("numberOfPersons")  # correct name
      number_km=int(km)
      travel_plan=models.travel_plan.objects.create(
         host=host,
         starting_point=starting_point,
         ending_point=ending_point,
         date_range=date_range,
         start_time=start_time,
         km=number_km,
         number_of_persons=number_of_persons,
      )
      host_user=User.objects.get(username=host)

      models.Joined_Members.objects.create(
         user=host_user,
         travelplan=travel_plan
      )
      travel_plan.joined_members=1
      travel_plan.save()
      
      travels=models.travel_plan.objects.all()
      add_points = models.Points.objects.get(user=host_user)
      added=travel_plan.km
      add_points.points +=added

      add_points.save()
      return redirect("home")
   return render(request,"biker/create.html",{"user":user})
def leaderboard(request):
    all_users = User.objects.all()
    
    # Ensure every user has a Points entry
    for user in all_users:
        models.Points.objects.get_or_create(user=user, defaults={'points': 0})
    
    # Filter users with points > 0 and order by descending points
    users_with_points = models.Points.objects.filter(points__gt=0).order_by('-points')
    
    context = {
        'users_with_points': users_with_points
    }
    return render(request, "biker/leaderboard.html", context)
def message(request,travel_id):
   if request.method=="POST":
      note=request.POST.get("note")
      current_user=User.objects.get(username=request.user.username)
      travel=models.travel_plan.objects.get(pk=travel_id)
      models.Notes.objects.create(
         current_user=current_user,
         add_notes=note,
         travel_post=travel,
      )
      return redirect("home")
   return render(request,"biker/message.html",{"travel_id":travel_id})
def milage(request):
   bike_info=models.bike_info.objects.first()
   models.bike_info.objects.all().delete()
   return render(request,"biker/milage.html",{"bike_info":bike_info})
# def joined_member(request):
#    if request.method=="POST":


# # class JoinTravelPlanAPI(APIView):
# #     def post(self, request):
# #         travel_id=request.data.get("id")
# #         current_user=User.objects.get(request.user.username)
# #         plan=models.travel_plan.objects.get(pk=travel_id)

# #         if models.Joined_Members.objects.filter(user=current_user,travelplan=plan).exists():
# #            return redirect("home")
# #         models.Joined_Members.objects.create(user=current_user,travelplan=plan)
# #         return redirect("home")
def join_travel(request):
   if request.method=="POST":
      travel_id=request.POST.get("id")
      current_user=User.objects.get(username=request.user.username)
      plan=models.travel_plan.objects.get(pk=travel_id)

      if models.Joined_Members.objects.filter(user=current_user,travelplan=plan).exists():
         return redirect("home")
      models.Joined_Members.objects.create(user=current_user,travelplan=plan)
      plan.joined_members+=1
      plan.save()
      
      return redirect("home")
def see_notes(request,notes_id):
   travel_post=travel_plan.objects.get(pk=notes_id)
   notes=models.Notes.objects.filter(travel_post=travel_post)
   return render(request,"biker/see_notes.html",{"notes":notes})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import travel_plan
from django.contrib.auth.models import User

@login_required
def my_t(request):
    current_user = User.objects.get(username=request.user.username)
    travels = travel_plan.objects.filter(host=current_user)

    if request.method == "POST":
        tid = request.POST.get("id")
        travel = travel_plan.objects.get(pk=tid)
        
        # Avoid duplicates in History
      #   if not History.objects.filter(plan=travel, user=current_user).exists():
      #       History.objects.create(plan=travel, user=current_user)
        
        return redirect('my_t')  # Redirect to prevent form re-submission

    # Get list of completed travel IDs for this user
   #  completed_ids = History.objects.filter(user=current_user).values_list('plan__id', flat=True)

    return render(request, "biker/my_t.html", {
        "travels": travels,
      #   "completed_ids": list(completed_ids),
    })
 