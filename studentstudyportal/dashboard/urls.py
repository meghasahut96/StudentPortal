from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('notes/',views.notes,name="notes"),
    path('delete_note/<int:pk>',views.delete,name="delete_note"),
    path('notes_Detail/<int:pk>',views.NoteDetailView.as_view(),name="notes_detail"),
    path('homework/',views.homework,name="homework"),
    path('update_homework/<int:pk>',views.update_homework,name="update_homework"),
    path('delete_homework/<int:pk>',views.delete_homework,name="delete_homework"),
    path('youtube/',views.youtube,name="youtube"),
    path('todo/',views.todo,name="todo"),
    path('update_todo/<int:pk>',views.update_todo,name="update_todo"),
    path('delete_todo/<int:pk>',views.delete_todo,name="delete_todo"),
    path('books/',views.books,name="books"),
    path('dictionary/',views.dictionary,name="dictionary"),
    path('conversion/',views.conversion,name="conversion")

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
