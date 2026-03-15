from django.contrib import admin
from .models import StudentProfile, Document, Grade, Schedule, Notification, ProblemSolution


@admin.register(ProblemSolution)
class ProblemSolutionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'is_active', 'order', 'updated_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['topic', 'keywords', 'solution']
    ordering = ['order', 'topic']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'course', 'specialty']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doc_type', 'status', 'created_at']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'score', 'status']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'time_start', 'time_end', 'subject', 'course']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
