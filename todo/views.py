from django.utils.timezone import now
from rest_framework import viewsets
from .models import TodoList, TodoCard, LastSaved
from .serializers import ToDoListSerializer, ToDoCardSerializer, LastSavedSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

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

    @action(detail=False, methods=["post"])
    def sync(self, request):
        """Clear all to-do lists and cards, then add the new ones."""
        # Clear the TodoList and TodoCard tables
        TodoList.objects.all().delete()
        TodoCard.objects.all().delete()

        # Get new TodoLists and TodoCards from request data
        todo_lists_data = request.data.get("lists", [])
        todo_cards_data = request.data.get("cards", [])
        
        try:
            # Bulk create new TodoLists
            todo_lists = [TodoList(**data) for data in todo_lists_data]
            TodoList.objects.bulk_create(todo_lists)

            # Now that TodoLists are created, we need to assign the correct TodoList instance to TodoCard's foreign key
            for card_data in todo_cards_data:
                # Fetch the corresponding TodoList instance by ID
                todo_list_instance = TodoList.objects.get(id=card_data["listId"])

                # Assign the TodoList instance to the card's foreign key
                card_data["listId"] = todo_list_instance

            # Bulk create new TodoCards with correct foreign key relationship
            todo_cards = [TodoCard(**data) for data in todo_cards_data]
            TodoCard.objects.bulk_create(todo_cards)

            # Update the last saved timestamp
            update_last_saved()

            return Response({"success": True}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

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