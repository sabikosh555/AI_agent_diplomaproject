"""
Cabinet app - function-based views
AI Advisor hybrid architecture:
dataset → admin FAQ → OpenAI → fallback
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
import os


# =========================
# LOGIN / REGISTER
# =========================

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('cabinet:staff_dashboard')
        return redirect('cabinet:assistant')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('cabinet:staff_dashboard')

            return redirect('cabinet:assistant')

        messages.error(request, 'Қате логин немесе пароль.')

    return render(request, 'cabinet/login.html')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('cabinet:assistant')

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Бұл username бос емес.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)
            return redirect('cabinet:assistant')

    return render(request, 'cabinet/register.html')


def logout_view(request):
    logout(request)
    return redirect('main:index')


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard_view(request):
    return render(request, 'cabinet/dashboard.html')


@login_required
def assistant_view(request):
    return render(request, 'cabinet/assistant.html')


# =========================
# DATASET LOADER
# =========================

FAQ_PATH = os.path.join(
    os.path.dirname(__file__),
    "faq_dataset.json"
)


def load_dataset():

    if not os.path.exists(FAQ_PATH):
        return []

    with open(FAQ_PATH, encoding="utf-8") as f:
        return json.load(f)


FAQ_DATASET = load_dataset()


# =========================
# DATASET SEARCH
# =========================

def get_dataset_response(message):

    text = message.lower()

    for item in FAQ_DATASET:

        if item["question"].lower() in text:
            return item["answer"]

        for keyword in item["keywords"]:
            if keyword.lower() in text:
                return item["answer"]

    return None


# =========================
# ADMIN FAQ SEARCH
# =========================

def get_db_semantic_response(message):

    from cabinet.models import ProblemSolution

    text = message.lower()

    solutions = ProblemSolution.objects.filter(is_active=True)

    for sol in solutions:

        if sol.keywords:

            keywords = sol.keywords.lower().split(",")

            for kw in keywords:

                if kw.strip() in text:
                    return sol.solution

    return None


# =========================
# OPENAI RESPONSE
# =========================

def get_openai_response(message):

    api_key = getattr(settings, "OPENAI_API_KEY", None)

    if not api_key:
        return None

    try:

        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content":
                    "Сен Қазақ ұлттық қыздар педагогикалық университетінің AI эдвайзерісің. "
                    "Студенттерге қысқа әрі нақты қазақ тілінде жауап бер."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None


# =========================
# FALLBACK RESPONSES
# =========================

AI_RESPONSES = {

      # Сәлемдесу
    "сәлем": "Сәлеметсіз бе! Қандай сұрағыңыз бар? Университет туралы ақпарат беруге дайынмын.",
    "салем": "Сәлеметсіз бе! Қандай сұрағыңыз бар? Университет туралы ақпарат беруге дайынмын.",
    "сәлемм": "Сәлеметсіз бе! Қандай сұрағыңыз бар? Университет туралы ақпарат беруге дайынмын.",
    "салемм": "Сәлеметсіз бе! Қандай сұрағыңыз бар? Университет туралы ақпарат беруге дайынмын.",
    "сәлеем": "Сәлеметсіз бе! Қандай сұрағыңыз бар? Университет туралы ақпарат беруге дайынмын.",
    "привет": "Сәлем! Қандай ақпарат қажет?",
    "прив": "Сәлем! Қандай ақпарат қажет?",
    "hello": "Hello! How can I help you with university information?",
    "hi": "Hello! How can I help you with university information?",
    "hey": "Hello! How can I help you with university information?",
    "здраствуйте": "Сәлеметсіз бе! Қалай көмектесе аламын?",
    "здравствуйте": "Сәлеметсіз бе! Қалай көмектесе аламын?",
    "ассалаумагалейкум": "Уағалейкумассалам! Қалай көмектесе аламын?",
    "ассаламағалейкум": "Уағалейкумассалам! Қалай көмектесе аламын?",

    # Рахмет
    "рахмет": "Сізге көмектесе алғаныма қуаныштымын! Тағы сұрақтарыңыз болса жазыңыз 😊",
    "ракмет": "Сізге көмектесе алғаныма қуаныштымын! Тағы сұрақтарыңыз болса жазыңыз 😊",
    "ракмеет": "Сізге көмектесе алғаныма қуаныштымын! Тағы сұрақтарыңыз болса жазыңыз 😊",
    "спасибо": "Қуаныштымын! Қосымша сұрақтарыңыз болса сұраңыз.",
    "спс": "Қуаныштымын! Қосымша сұрақтарыңыз болса сұраңыз.",
    "thanks": "Glad to help! Feel free to ask more questions.",
    "thx": "Glad to help! Feel free to ask more questions.",
    "thank you": "Glad to help! Feel free to ask more questions.",

    # Көмек сұрау
    "көмек": "Қандай мәселе бойынша ақпарат қажет? Мамандықтар, грант, жатақхана немесе қабылдау туралы сұрай аласыз.",
    "комек": "Қандай мәселе бойынша ақпарат қажет? Мамандықтар, грант, жатақхана немесе қабылдау туралы сұрай аласыз.",
    "кмек": "Қандай мәселе бойынша ақпарат қажет? Мамандықтар, грант, жатақхана немесе қабылдау туралы сұрай аласыз.",
    "көмектес": "Қандай мәселе бойынша ақпарат қажет? Мамандықтар, грант, жатақхана немесе қабылдау туралы сұрай аласыз.",
    "комектес": "Қандай мәселе бойынша ақпарат қажет? Мамандықтар, грант, жатақхана немесе қабылдау туралы сұрай аласыз.",
    "помощь": "Қандай ақпарат қажет екенін нақтылап жазыңыз.",
    "help": "Please specify what kind of university information you need.",
    "сұрақ": "Сұрағыңызды жазыңыз, көмектесуге тырысамын.",
    "вопрос": "Қандай сұрағыңыз бар?",
}


def get_local_ai_response(message):

    text = message.lower()

    for key, value in AI_RESPONSES.items():

        if key in text:
            return value

    return "Бұл сұрақ бойынша нақты ақпарат табылмады. Деканатқа хабарласыңыз."


# =========================
# CHAT API VIEW
# =========================

@login_required
@require_http_methods(["POST"])
def chat_api_view(request):

    try:

        data = json.loads(request.body)

        message = data.get("message")

        if not message:
            return JsonResponse(
                {"error": "Message empty"},
                status=400
            )

        # 1️⃣ dataset search

        response = get_dataset_response(message)

        # 2️⃣ admin faq

        if not response:
            response = get_db_semantic_response(message)

        # 3️⃣ openai fallback

        if not response:
            response = get_openai_response(message)

        # 4️⃣ local fallback

        if not response:
            response = get_local_ai_response(message)

        return JsonResponse({
            "response": response
        })

    except Exception as e:

        return JsonResponse(
            {"error": str(e)},
            status=500
        )
@login_required
def documents_view(request):
    return render(request, 'cabinet/documents.html')
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def documents_view(request):
    return render(request, "cabinet/documents.html")


@login_required
def document_create_view(request):
    return render(request, "cabinet/document_create.html")


@login_required
def profile_view(request):
    return render(request, "cabinet/profile.html")


@login_required
def settings_view(request):
    return render(request, "cabinet/settings.html")
@login_required
def schedule_view(request):
    return render(request, "cabinet/schedule.html")
@login_required
def deanoffice_view(request):
    return render(request, "cabinet/deanoffice.html")
@login_required
def grades_view(request):
    return render(request, "cabinet/grades.html")
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_view(request):
    return render(request, "cabinet/dashboard.html")


@login_required
def documents_view(request):
    return render(request, "cabinet/documents.html")


@login_required
def document_create_view(request):
    return render(request, "cabinet/document_create.html")


@login_required
def schedule_view(request):
    return render(request, "cabinet/schedule.html")


@login_required
def deanoffice_view(request):
    return render(request, "cabinet/deanoffice.html")


@login_required
def grades_view(request):
    return render(request, "cabinet/grades.html")


@login_required
def notifications_view(request):
    return render(request, "cabinet/notifications.html")


@login_required
def profile_view(request):
    return render(request, "cabinet/profile.html")


@login_required
def settings_view(request):
    return render(request, "cabinet/settings.html")