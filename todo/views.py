from django.utils.timezone import now
from rest_framework import viewsets
from .models import ToDoList, ToDoListCard, LastSaved
from .serializers import ToDoListSerializer, ToDoListCardSerializer, LastSavedSerializer
from rest_framework.response import Response

def update_last_saved():
    """Updates the last saved timestamp in the database."""
    obj, _ = LastSaved.objects.get_or_create(id=1)
    obj.timestamp = now()
    obj.save()


class LastSavedMixin:
    """Mixin to update last saved timestamp after create, update, and delete"""
    
    def perform_create(self, serializer):
        serializer.save()
        update_last_saved()

    def perform_update(self, serializer):
        serializer.save()
        update_last_saved()

    def perform_destroy(self, instance):
        instance.delete()
        update_last_saved()

class ToDoListViewSet(LastSavedMixin, viewsets.ModelViewSet):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer

class ToDoListCardViewSet(LastSavedMixin, viewsets.ModelViewSet):
    queryset = ToDoListCard.objects.all()
    serializer_class = ToDoListCardSerializer

class LastSavedViewSet(viewsets.ViewSet):
    def list(self, request):
        """Retrieve the last saved timestamp"""
        obj, _ = LastSaved.objects.get_or_create(id=1)
        serializer = LastSavedSerializer(obj)
        return Response(serializer.data)