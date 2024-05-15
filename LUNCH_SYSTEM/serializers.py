from django.contrib.auth.models import User
from rest_framework import serializers
from LUNCH_SYSTEM.models import Restaurant, Menu, Employee, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Menu
        fields = "__all__"

    def create(self, validated_data):
        items = validated_data.pop('items')
        menus = []
        for item in items:
            menu = Menu.objects.create(items=item, **validated_data)
            menus.append(menu)
        return menus

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = instance.items.split(",")
        return representation


class GroupedMenuSerializer(serializers.Serializer):
    pass


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class EmployeeSerializer(serializers.ModelSerializer):
    user = EmployeeUserSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'department', 'position')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        return employee


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'restaurant', 'date')

    def validate_employee_id(self, value):
        if not value.employee:
            raise serializers.ValidationError("Employee associated with token does not exist.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        employee = user.employee
        vote_date = data['date']
        existing_votes = Vote.objects.filter(employee=employee, date=vote_date)
        if self.instance:
            existing_votes = existing_votes.exclude(pk=self.instance.pk)
        if existing_votes.exists():
            raise serializers.ValidationError("A vote already exists for this employee and date.")
        return data


class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'day_of_week', 'restaurant')
