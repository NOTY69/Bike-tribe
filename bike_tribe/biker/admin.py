from django.contrib import admin
from .models import travel_plan, Joined_Members, bike_info, Notes, Points
# Register your models here.
admin.site.register(travel_plan)
admin.site.register(Joined_Members)
admin.site.register(bike_info)
admin.site.register(Notes)
admin.site.register(Points)