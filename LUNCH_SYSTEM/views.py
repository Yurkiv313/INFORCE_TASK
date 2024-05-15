from datetime import datetime

import pytz
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Restaurant, Menu, Employee, Vote
from .serializers import RestaurantSerializer, MenuSerializer, GroupedMenuSerializer, EmployeeSerializer, \
    VoteSerializer, MenusSerializer


def index(request):
    return HttpResponse("Hello, world!")


@extend_schema(request=RestaurantSerializer, responses={200: RestaurantSerializer(many=True)})
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False)
    def get_restaurant(self, request):
        restaurant = Restaurant.objects.all()
        serializer = self.get_serializer(restaurant, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def create_restaurant(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=MenuSerializer, responses={200: MenuSerializer(many=True)})
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(detail=False)
    def get_menus(self, request):
        menus = Menu.objects.create()
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def create_menu(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            menus = serializer.save()
            return Response(MenuSerializer(menus, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def todays_menu(self, request):
        ukraine_tz = pytz.timezone('Europe/Kiev')
        day_of_week = datetime.now(ukraine_tz).isoweekday()

        menus = Menu.objects.filter(day_of_week=day_of_week)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


@extend_schema(request=GroupedMenuSerializer, responses={200: GroupedMenuSerializer()})
class MenuViews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_menu_by_day_of_week(self, request, pk):
        restaurants = Restaurant.objects.filter(menus__day_of_week=pk).all().all()
        grouped_menus = []
        for restaurant in restaurants:
            if not any("restaurantId" in obj and obj["restaurantId"] == restaurant.id for obj in grouped_menus):
                menuItems = [obj.items for obj in list(restaurant.menus.all())]
                grouped_menus.append(
                    {"restaurantId": restaurant.id, "restaurantName": restaurant.name, "menu": menuItems})

        return JsonResponse(grouped_menus, safe=False)


@extend_schema(request=EmployeeSerializer, responses={200: EmployeeSerializer(many=True)})
class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(request=VoteSerializer, responses={200: VoteSerializer(many=True)})
class VoteUpsertAPIView(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False)
    def get_object(self):

        user = self.request.user
        date = self.request.data.get('date')
        try:
            return Vote.objects.get(employee=user.employee, date=date)
        except Vote.DoesNotExist:
            return None

    @action(detail=False)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            return self.update(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=self.request.user.employee)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MostVotedRestaurantMenuAPIView(viewsets.ModelViewSet):
    def get(self, request):
        ukraine_tz = pytz.timezone('Europe/Kiev')
        current_date = datetime.now(ukraine_tz)

        most_voted_restaurant = Vote.objects.filter(date=current_date).values('restaurant').annotate(
            vote_count=Count('restaurant')).order_by('-vote_count').first()

        if most_voted_restaurant:
            most_voted_restaurant_id = most_voted_restaurant['restaurant']
            menu = Menu.objects.filter(day_of_week=current_date.weekday(), restaurant_id=most_voted_restaurant_id).first()
            if menu:
                serializer = MenusSerializer(menu)
                return Response(serializer.data)

        return Response({"message": "No menu found for the most voted restaurant of the current day."},
                        status=status.HTTP_404_NOT_FOUND)
