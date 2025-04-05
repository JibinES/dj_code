# api/admin.py

from django.contrib import admin
from .models import Problem, UserProfile, ChatMessage, CodeSubmission, UploadedFile

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'related_topics', 'created_at')
    list_filter = ('difficulty', 'related_topics')
    search_fields = ('title', 'description', 'related_topics')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'preferred_topics')
    search_fields = ('user__username', 'preferred_topics')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_type', 'content_preview', 'timestamp')
    list_filter = ('message_type', 'timestamp')
    search_fields = ('user__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'is_correct', 'submitted_at')
    list_filter = ('language', 'is_correct', 'submitted_at')
    search_fields = ('user__username', 'problem__title', 'code')

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('user__username', 'file_name')