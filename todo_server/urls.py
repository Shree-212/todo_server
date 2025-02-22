from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import ToDoListViewSet, ToDoListCardViewSet, LastSavedViewSet

router = DefaultRouter()
router.register(r'todo-lists', ToDoListViewSet)
router.register(r'todo-cards', ToDoListCardViewSet)

print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('last-saved/', LastSavedViewSet.as_view({'get': 'list'})),
]