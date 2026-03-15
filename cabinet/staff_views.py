"""
Университет әкімшілігі - staff views
Тек is_staff пайдаланушыларға қол жетімді
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Document, Grade, Schedule, StudentProfile, ProblemSolution


def staff_required(view_func):
    """Тек staff пайдаланушыларға рұқсат."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('cabinet:login')
        if not request.user.is_staff:
            messages.error(request, 'Қол жетімсіз.')
            return redirect('main:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@staff_required
def staff_dashboard_view(request):
    """Университет басты панелі."""
    from django.db.models import Count
    students_count = User.objects.filter(is_staff=False).count()
    docs_pending = Document.objects.filter(status='pending').count()
    return render(request, 'cabinet/staff/dashboard.html', {
        'active_page': 'dashboard',
        'students_count': students_count,
        'docs_pending': docs_pending,
    })


@login_required
@staff_required
def staff_students_view(request):
    """Студенттер тізімі."""
    students = User.objects.filter(is_staff=False).select_related('student_profile').order_by('id')
    return render(request, 'cabinet/staff/students.html', {'active_page': 'students', 'students': students})


@login_required
@staff_required
def staff_documents_view(request):
    """Құжат сұраулары (заявки)."""
    documents = Document.objects.select_related('user').order_by('-created_at')
    return render(request, 'cabinet/staff/documents.html', {'active_page': 'documents', 'documents': documents})


@login_required
@staff_required
def staff_document_status_view(request, pk):
    """Құжат мәртебесін өзгерту."""
    doc = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'ready']:
            doc.status = status
            doc.save()
            messages.success(request, 'Мәртебе өзгертілді.')
        return redirect('cabinet:staff_documents')
    return redirect('cabinet:staff_documents')


@login_required
@staff_required
def staff_grades_view(request):
    """Бағаларды басқару."""
    grades = Grade.objects.select_related('user').order_by('-id')[:100]
    return render(request, 'cabinet/staff/grades.html', {'active_page': 'grades', 'grades': grades})


@login_required
@staff_required
def staff_grade_add_view(request):
    """Баға қосу."""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        subject = request.POST.get('subject', '').strip()
        score = request.POST.get('score')
        user = get_object_or_404(User, id=user_id)
        if subject:
            score_val = int(score) if score and score.isdigit() else None
            Grade.objects.create(user=user, subject=subject, score=score_val, status='Өтті')
            messages.success(request, 'Баға қосылды.')
        return redirect('cabinet:staff_grades')
    students = User.objects.filter(is_staff=False).order_by('username')
    return render(request, 'cabinet/staff/grade_add.html', {'active_page': 'grades', 'students': students})


@login_required
@staff_required
def staff_schedule_view(request):
    """Кесте басқару."""
    schedule = Schedule.objects.all().order_by('day', 'time_start')
    return render(request, 'cabinet/staff/schedule.html', {'active_page': 'schedule', 'schedule': schedule})


@login_required
@staff_required
def staff_schedule_add_view(request):
    """Кестеге қосу."""
    if request.method == 'POST':
        day = request.POST.get('day')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')
        subject = request.POST.get('subject', '').strip()
        course = request.POST.get('course', 3)
        if day and time_start and time_end and subject:
            Schedule.objects.create(
                day=int(day),
                time_start=time_start,
                time_end=time_end,
                subject=subject,
                course=int(course) if course else 3,
            )
            messages.success(request, 'Кестеге қосылды.')
        return redirect('cabinet:staff_schedule')
    return render(request, 'cabinet/staff/schedule_add.html', {'active_page': 'schedule'})


# === Мәселе шешімдері (AI көмекші үшін) ===

@login_required
@staff_required
def staff_solutions_view(request):
    """Мәселе шешімдері — AI көмекші сұрақтарға жауап беруде осыны пайдаланады."""
    solutions = ProblemSolution.objects.all().order_by('order', 'topic')
    return render(request, 'cabinet/staff/solutions.html', {
        'active_page': 'solutions',
        'solutions': solutions,
    })


@login_required
@staff_required
def staff_solution_add_view(request):
    """Мәселе шешімін қосу."""
    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()
        keywords = request.POST.get('keywords', '').strip()
        solution = request.POST.get('solution', '').strip()
        if topic and solution:
            order = 0
            last = ProblemSolution.objects.order_by('-order').first()
            if last:
                order = last.order + 1
            ProblemSolution.objects.create(
                topic=topic,
                keywords=keywords,
                solution=solution,
                order=order,
            )
            messages.success(request, 'Шешім қосылды. AI көмекші енді осы ақпаратты пайдаланады.')
            return redirect('cabinet:staff_solutions')
        messages.error(request, 'Тақырып пен шешім міндетті.')
    return render(request, 'cabinet/staff/solution_form.html', {
        'active_page': 'solutions',
        'solution': None,
    })


@login_required
@staff_required
def staff_solution_edit_view(request, pk):
    """Мәселе шешімін өзгерту."""
    sol = get_object_or_404(ProblemSolution, pk=pk)
    if request.method == 'POST':
        sol.topic = request.POST.get('topic', '').strip()
        sol.keywords = request.POST.get('keywords', '').strip()
        sol.solution = request.POST.get('solution', '').strip()
        sol.is_active = request.POST.get('is_active') == 'on'
        try:
            sol.order = int(request.POST.get('order', 0))
        except ValueError:
            pass
        if sol.topic and sol.solution:
            sol.save()
            messages.success(request, 'Шешім сақталды.')
            return redirect('cabinet:staff_solutions')
        messages.error(request, 'Тақырып пен шешім міндетті.')
    return render(request, 'cabinet/staff/solution_form.html', {
        'active_page': 'solutions',
        'solution': sol,
    })


@login_required
@staff_required
def staff_solution_delete_view(request, pk):
    """Мәселе шешімін өшіру."""
    sol = get_object_or_404(ProblemSolution, pk=pk)
    if request.method == 'POST':
        sol.delete()
        messages.success(request, 'Шешім өшірілді.')
        return redirect('cabinet:staff_solutions')
    return redirect('cabinet:staff_solutions')
