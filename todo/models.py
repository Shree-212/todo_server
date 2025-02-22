from django.db import models
import uuid

class LastSaved(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

class TodoList(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    name = models.CharField(max_length=255)

class TodoCard(models.Model):
    id = models.UUIDField(primary_key=True, editable=True)
    text = models.TextField()
    listId = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="cards")
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)