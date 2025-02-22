from django.db import models

class LastSaved(models.Model):
    timestamp = models.DateTimeField(auto_now=True)

class ToDoList(models.Model):
    name = models.CharField(max_length=255)

class ToDoListCard(models.Model):
    categoryId = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name="cards")
    text = models.TextField()
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)