from django.utils.timezone import now
from rest_framework import viewsets
from .models import TodoList, TodoCard, LastSaved
from .serializers import ToDoListSerializer, ToDoCardSerializer, LastSavedSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

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

class ToDoListViewSet(LastSavedMixin, viewsets.ModelViewSet):
    queryset = TodoList.objects.all()
    serializer_class = ToDoListSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True}, status=HTTP_200_OK)

class ToDoCardViewSet(LastSavedMixin, viewsets.ModelViewSet):
    queryset = TodoCard.objects.all()
    serializer_class = ToDoCardSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"success": True}, status=HTTP_200_OK)

class LastSavedViewSet(viewsets.ViewSet):
    def list(self, request):
        """Retrieve the last saved timestamp"""
        obj, _ = LastSaved.objects.get_or_create(id=1)
        serializer = LastSavedSerializer(obj)
        return Response(serializer.data)