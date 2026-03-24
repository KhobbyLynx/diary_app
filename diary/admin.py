from django.contrib import admin
from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'emotion']
    list_filter = ['created_at', 'emotion', 'user']
    search_fields = ['title', 'content']
