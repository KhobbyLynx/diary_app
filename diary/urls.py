from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/create/', views.entry_create, name='entry_create'),
    path('entry/<int:pk>/update/', views.entry_update, name='entry_update'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('entry/<int:pk>/analyze/', views.analyze_entry_by_id, name='analyze_entry_by_id'),
    path('api/analyze/', views.analyze_entry, name='analyze_entry'),
]
