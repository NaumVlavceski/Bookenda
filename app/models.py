from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    types=[
        ("Business","Business"),
        ("Sports","Sports"),
        ("Charity","Charity"),
        ("Councils","Councils"),
        ("Academic","Academic"),
        ("Cultural","Cultural"),
        ("Community","Community"),
        ("Concert","Concert")
    ]
    title = models.CharField(max_length=100)
    type = models.CharField(choices=types, max_length=100)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.IntegerField()
    price = models.FloatField()
    free_seats = models.IntegerField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="events")
    photo = models.ImageField(upload_to="events/")

    def __str__(self):
        return self.title

class Reservation(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    seat_reservation = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + " " + self.event.title
