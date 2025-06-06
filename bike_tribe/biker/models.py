from django.db import models
from django.contrib.auth.models import User

class travel_plan(models.Model):
    host = models.CharField(max_length=100)
    starting_point = models.CharField(max_length=255)
    ending_point = models.CharField(max_length=255)
    date_range = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    km = models.IntegerField()
    number_of_persons = models.PositiveIntegerField()
    joined_members = models.PositiveIntegerField(default=0)  # This is just a count

    def __str__(self):
        return f"{self.starting_point} to {self.ending_point} on {self.date_range}"


class Joined_Members(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travelplan = models.ForeignKey(travel_plan, on_delete=models.CASCADE, related_name="member_entries")

    def __str__(self):
        return f"{self.user.username} joined {self.travelplan}"


class bike_info(models.Model):
    bike_name = models.CharField(max_length=100)
    cc = models.CharField(max_length=10)
    km = models.FloatField()

    def __str__(self):
        return f"{self.bike_name} - {self.cc}cc - {self.km}km"


class Notes(models.Model):
    current_user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_notes = models.TextField()
    travel_post = models.ForeignKey(travel_plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note by {self.current_user.username} on {self.travel_post}"


# Optional: Uncomment and use this if you want to implement trip history
# class History(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     plan = models.ForeignKey(travel_plan, on_delete=models.CASCADE)
#     completed_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} completed {self.plan}"
class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} has {self.points} points"