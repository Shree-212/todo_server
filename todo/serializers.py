from rest_framework import serializers
from .models import ToDoList, ToDoListCard, LastSaved

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'

class ToDoListCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoListCard
        fields = '__all__'

class LastSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastSaved
        fields = '__all__'