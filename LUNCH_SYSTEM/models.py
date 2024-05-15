from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menus", on_delete=models.CASCADE)
    day_of_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    items = models.TextField()

    def __str__(self):
        return f"{self.restaurant.name} - {self.day_of_week}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def str(self):
        return self.user.username


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('employee', 'date')

    def str(self):
        return f"{self.employee} voted for {self.restaurant} on {self.date}"
