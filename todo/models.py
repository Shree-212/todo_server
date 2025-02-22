from django.db import models

class LastSaved(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

class TodoList(models.Model):
    name = models.CharField(max_length=255)

class TodoCard(models.Model):
    text = models.TextField()
    listId = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="cards")
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)