from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from LUNCH_SYSTEM.models import Restaurant, Menu, Employee, Vote
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        Restaurant.objects.all().delete()
        Menu.objects.all().delete()
        Employee.objects.all().delete()
        Vote.objects.all().delete()

        restaurants = ['Restaurant A', 'Restaurant B', 'Restaurant C']
        for restaurant_name in restaurants:
            restaurant, _ = Restaurant.objects.get_or_create(name=restaurant_name)

        for restaurant in Restaurant.objects.all():
            for day_of_week in range(1, 8):
                menu_items = f"Menu items for {restaurant.name} on day {day_of_week}"
                menu, _ = Menu.objects.get_or_create(restaurant=restaurant, day_of_week=day_of_week, items=menu_items)

        for i in range(1, 6):
            user = User.objects.create(username=f'user{i}')
            employee = Employee.objects.create(user=user, department=f'Department {i}', position=f'Position {i}')

        employees = Employee.objects.all()
        for employee in employees:
            date = timezone.now().date()
            restaurant = Restaurant.objects.all().order_by('?').first()
            vote = Vote.objects.create(employee=employee, restaurant=restaurant, date=date)

        self.stdout.write(self.style.SUCCESS('Sample data created successfully'))
