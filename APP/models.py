from django.db import models
from django.contrib.auth.models import User
import datetime 

class Room(models.Model):
    Type = (
        ('Single Room','Single Room'),
        ('Family Room','Family Room'),
        ('Presidential Room','Presidential Room'),
    )
    room_type=models.CharField(max_length=50,choices=Type)
    room_number = models.CharField(max_length=10,unique=True)
    booked_checkin_date = models.DateTimeField(null=True)
    booked_checkout_date = models.DateTimeField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Room_image=models.ImageField(upload_to='photos/Rooms',default='default_room_image.jpg')
    is_booked=models.BooleanField(default=False)
    # Add other room details like room type, amenities, etc. as needed

    def __str__(self):
        return self.room_type           

class Ticket(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    no_of_rooms = models.IntegerField(default=0)
    check_in_date = models.DateField()
    check_in_time = models.TimeField(default=datetime.time(0, 0))
    check_out_date = models.DateField()
    is_checked_out = models.BooleanField(default=False)
    # Add other ticket details like payment information, special requests, etc. as needed

    def __str__(self):
        return f"{self.room} - {self.check_in_date} to {self.check_out_date}"

class Users(models.Model):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    Email=models.CharField(max_length=50)
    proof=models.ImageField(upload_to='photos/user')
    ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE)

class Payment(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)

    # Add other payment details like payment method, transaction ID, etc. as needed

    def __str__(self):
        return f"{self.ticket} - Paid: {self.amount}"

