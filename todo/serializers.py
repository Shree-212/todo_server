from rest_framework import serializers
from .models import TodoList, TodoCard, LastSaved

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = '__all__'

class ToDoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCard
        fields = '__all__'

class LastSavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastSaved
        fields = '__all__'