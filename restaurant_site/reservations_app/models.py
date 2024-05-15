from django.db import models
from datetime import timezone
from django.core.exceptions import ValidationError
from user_management.models import User
from datetime import datetime


def validate_date(date):
    if date < timezone.now().date():
        raise ValidationError("Date cannot be in the past")

class Table(models.Model):
    no_of_seats = models.PositiveIntegerField(null=False)
    
    def __str__(self):
        return f"Table number {self.id}, capacity: {self.no_of_seats}"
    


class Reservation(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(validators=[validate_date])
    table = models.ForeignKey(Table, related_name='reservations', blank=True, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, related_name='reservations', blank=True, on_delete=models.CASCADE)
    seats_needed = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f"A reservation from {self.time} to {self.end_time} for table number {self.table} for {self.seats_needed} people."