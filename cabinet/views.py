"""
Cabinet app - function-based views
"""
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


def login_view(request):
    """Страница входа в личный кабинет."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('cabinet:staff_dashboard')
        return redirect('cabinet:assistant')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_staff:
                return redirect('cabinet:staff_dashboard')
            return redirect('cabinet:assistant')
        else:
            messages.error(request, 'Пайдаланушы аты немесе құпия сөз қате.')

    return render(request, 'cabinet/login.html')


def register_view(request):
    """Тіркелу беті."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('cabinet:staff_dashboard')
        return redirect('cabinet:assistant')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        errors = []
        if not username:
            errors.append('Пайдаланушы атын енгізіңіз.')
        if User.objects.filter(username=username).exists():
            errors.append('Бұл пайдаланушы аты қолданылып жатыр.')
        if not email:
            errors.append('Электрондық поштаны енгізіңіз.')
        if User.objects.filter(email=email).exists():
            errors.append('Бұл пошта тіркелген.')
        if len(password1) < 6:
            errors.append('Құпия сөз кем дегенде 6 таңбадан тұруы керек.')
        if password1 != password2:
            errors.append('Құпия сөздер сәйкес келмейді.')

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name or username,
                last_name=last_name,
            )
            from cabinet.models import StudentProfile
            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'student_id': f'2025-{user.id:06d}',
                    'course': 1,
                    'faculty': 'Ақпараттық технологиялар',
                    'specialty': 'Ақпараттық жүйелер',
                }
            )
            login(request, user)
            messages.success(request, 'Тіркелу сәтті аяқталды!')
            return redirect('cabinet:assistant')

    return render(request, 'cabinet/register.html')


def logout_view(request):
    """Выход из системы."""
    logout(request)
    return redirect('main:index')


@login_required
def dashboard_view(request):
    """Главная панель кабинета."""
    user = request.user
    profile = getattr(user, 'student_profile', None)
    documents_count = user.documents.count()
    notifications_count = user.notifications.filter(is_read=False).count()
    grades_count = user.grades.count()

    context = {
        'user': user,
        'profile': profile,
        'active_page': 'dashboard',
        'documents_count': documents_count,
        'notifications_count': notifications_count,
        'grades_count': grades_count,
    }
    return render(request, 'cabinet/dashboard.html', context)


@login_required
def documents_view(request):
    """Страница документов."""
    documents = request.user.documents.order_by('-created_at')
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/documents.html', {
        'documents': documents,
        'active_page': 'documents',
        'profile': profile,
    })


@login_required
def document_create_view(request):
    """Жаңа құжат сұрау."""
    if request.method == 'POST':
        from cabinet.models import Document
        doc_type = request.POST.get('doc_type', '').strip()
        if doc_type:
            Document.objects.create(
                user=request.user,
                doc_type=doc_type,
                status='pending',
            )
            messages.success(request, 'Құжат сұрауы жіберілді.')
        else:
            messages.error(request, 'Құжат түрін енгізіңіз.')
        return redirect('cabinet:documents')
    return redirect('cabinet:documents')


@login_required
def deanoffice_view(request):
    """Деканат контакттары — байланыс ақпараты."""
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/deanoffice.html', {
        'active_page': 'deanoffice',
        'profile': profile,
    })


@login_required
def schedule_view(request):
    """Страница расписания."""
    from cabinet.models import Schedule
    profile = getattr(request.user, 'student_profile', None)
    course = profile.course if profile else 3
    schedule = Schedule.objects.filter(course=course).order_by('day', 'time_start')
    return render(request, 'cabinet/schedule.html', {
        'active_page': 'schedule',
        'profile': profile,
        'schedule': schedule,
    })


@login_required
def assistant_view(request):
    """AI Көмекші - страница чата."""
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/assistant.html', {
        'active_page': 'assistant',
        'profile': profile,
    })


@login_required
def grades_view(request):
    """Страница оценок."""
    grades = request.user.grades.all()
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/grades.html', {
        'grades': grades,
        'active_page': 'grades',
        'profile': profile,
    })


@login_required
def notifications_view(request):
    """Страница уведомлений."""
    notifications = request.user.notifications.order_by('-created_at')
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/notifications.html', {
        'notifications': notifications,
        'active_page': 'notifications',
        'profile': profile,
    })


@login_required
def profile_view(request):
    """Страница профиля."""
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/profile.html', {
        'profile': profile,
        'active_page': 'profile',
    })


@login_required
def settings_view(request):
    """Страница настроек."""
    profile = getattr(request.user, 'student_profile', None)
    return render(request, 'cabinet/settings.html', {
        'active_page': 'settings',
        'profile': profile,
    })


# AI Chat API
AI_RESPONSES = {
    'сәлем': 'Сәлеметсіз бе! Қандай көмек керек?',
    'салем': 'Сәлеметсіз бе! Қандай көмек керек?',
    'келесі': 'Келесі сынып кестесін білу үшін деканатпен хабарласыңыз немесе студент порталын қараңыз.',
    'кесте': 'Кесте туралы ақпарат студент порталында немесе деканатта бар. Қосымша сұрағыңыз бар ма?',
    'құжат': 'Құжат сұрау үшін жеке кабинетке кіріп "Құжат сұрау" бөліміне өтіңіз.',
    'справка': 'Справка алу үшін деканатқа өтініш беріңіз. Жеке кабинет арқылы да сұрау жасауға болады.',
    'емтихан': 'Емтихан кестесі әдетте семестр соңында жарияланады. Нақты күндер туралы деканаттан хабарласыңыз.',
    'деканат': 'Деканатпен байланыс: пошта арқылы немесе жеке келу. Жұмыс уақыты: дүйсенбі-жұма 9:00-18:00.',
    'рахмет': 'Оқасы жоқ! Басқа сұрағыңыз болса, сұраңыз.',
    'көмек': 'Мен университет қызметі бойынша көмектесемін: кесте, құжаттар, процедуралар туралы сұрақтарға жауап бере аламын.',
    'баға': 'Бағаларыңызды көру үшін жеке кабинеттегі "Бағалар" бөліміне өтіңіз.',
    'балл': 'Бағаларыңызды көру үшін жеке кабинеттегі "Бағалар" бөліміне өтіңіз.',
    'сабақ': 'Сабақ кестесін "Кесте" бөлімінде көре аласыз.',
}


def get_solutions_context():
    """Админ қосқан мәселе шешімдерін алу — AI контексті үшін."""
    from cabinet.models import ProblemSolution
    solutions = ProblemSolution.objects.filter(is_active=True).order_by('order')[:20]
    if not solutions:
        return ''
    parts = ['Университет әкімшілігі қосқан мәселе шешімдері (осыны негізге алыңыз):']
    for s in solutions:
        parts.append(f'- {s.topic}: {s.solution}')
    return '\n'.join(parts)


def get_local_ai_response(text):
    """Локальды жауап (OpenAI жоқ кезде). Алдымен БД шешімдерін, кейін AI_RESPONSES қарайды."""
    from cabinet.models import ProblemSolution
    lower = text.lower().strip()

    # Админ қосқан шешімдерді кілт сөздер бойынша іздеу
    for sol in ProblemSolution.objects.filter(is_active=True).order_by('order'):
        if sol.keywords:
            for kw in sol.keywords.lower().replace(',', ' ').split():
                kw = kw.strip()
                if kw and kw in lower:
                    return sol.solution

    for key, value in AI_RESPONSES.items():
        if key in lower:
            return value
    return 'Түсінікті. Бұл сұрақ бойынша деканатпен немесе оқытушымен хабарласыңыз. Басқа сұрағыңыз бар ма?'


def get_openai_response(text, history=None):
    """OpenAI API арқылы жауап алу. history — [{role, content}, ...] сөйлесу тарихы."""
    api_key = getattr(settings, 'OPENAI_API_KEY', '') or ''
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        system_content = (
            'Сіз университет қызметі бойынша AI көмекшісіз. '
            'Құжаттар, кесте, процедуралар, деканат туралы сұрақтарға жауап беріңіз. '
            'Қазақ тілінде жауап беріңіз. Қысқа және түсінікті жауап беріңіз.'
        )
        solutions_ctx = get_solutions_context()
        if solutions_ctx:
            system_content += '\n\n' + solutions_ctx

        messages = [
            {'role': 'system', 'content': system_content},
        ]
        if history:
            for h in history[-10:]:  # соңғы 10 хабарлама
                messages.append({'role': h['role'], 'content': h['content']})
        messages.append({'role': 'user', 'content': text})

        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=500,
        )
        if response.choices:
            return response.choices[0].message.content.strip()
    except Exception as e:
        if settings.DEBUG:
            import logging
            logging.getLogger(__name__).warning('OpenAI API қатесі: %s', str(e))
    return None


@login_required
@require_http_methods(["POST"])
def chat_api_view(request):
    """API endpoint для AI чата - OpenAI немесе локальды жауап."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'Бос хабарлама'}, status=400)

        history = data.get('history', [])
        response_text = get_openai_response(message, history)
        if response_text is None:
            response_text = get_local_ai_response(message)

        return JsonResponse({'response': response_text})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Қате сұрау'}, status=400)
