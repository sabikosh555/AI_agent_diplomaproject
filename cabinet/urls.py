"""
Cabinet app URLs
"""
from django.urls import path
from . import views
from . import staff_views

app_name = 'cabinet'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('documents/', views.documents_view, name='documents'),
    path('documents/add/', views.document_create_view, name='document_create'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('deanoffice/', views.deanoffice_view, name='deanoffice'),
    path('assistant/', views.assistant_view, name='assistant'),
    path('grades/', views.grades_view, name='grades'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('api/chat/', views.chat_api_view, name='chat_api'),
    # Университет әкімшілігі (staff)
    path('staff/', staff_views.staff_dashboard_view, name='staff_dashboard'),
    path('staff/students/', staff_views.staff_students_view, name='staff_students'),
    path('staff/documents/', staff_views.staff_documents_view, name='staff_documents'),
    path('staff/documents/<int:pk>/status/', staff_views.staff_document_status_view, name='staff_document_status'),
    path('staff/grades/', staff_views.staff_grades_view, name='staff_grades'),
    path('staff/grades/add/', staff_views.staff_grade_add_view, name='staff_grade_add'),
    path('staff/schedule/', staff_views.staff_schedule_view, name='staff_schedule'),
    path('staff/schedule/add/', staff_views.staff_schedule_add_view, name='staff_schedule_add'),
    path('staff/solutions/', staff_views.staff_solutions_view, name='staff_solutions'),
    path('staff/solutions/add/', staff_views.staff_solution_add_view, name='staff_solution_add'),
    path('staff/solutions/<int:pk>/edit/', staff_views.staff_solution_edit_view, name='staff_solution_edit'),
    path('staff/solutions/<int:pk>/delete/', staff_views.staff_solution_delete_view, name='staff_solution_delete'),
]
