"""
Создание демо-данных для тестирования
python manage.py create_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cabinet.models import StudentProfile, Document, Grade, Notification


class Command(BaseCommand):
    help = 'Создает демо-пользователя и тестовые данные'

    def handle(self, *args, **options):
        # Staff/Admin user
        staff, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@university.kz',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if not staff.has_usable_password():
            staff.set_password('admin123')
            staff.save()
            self.stdout.write('Staff user: admin / admin123')

        user, created = User.objects.get_or_create(
            username='student',
            defaults={
                'email': 'student@university.kz',
                'first_name': 'Студент',
                'last_name': 'Аты',
            }
        )
        if created:
            user.set_password('student123')
            user.save()
            self.stdout.write(self.style.SUCCESS('User created: student / student123'))

        profile, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={
                'student_id': '2023-001234',
                'course': 3,
                'faculty': 'Ақпараттық технологиялар',
                'specialty': 'Ақпараттық жүйелер',
            }
        )

        if not user.documents.exists():
            Document.objects.bulk_create([
                Document(user=user, doc_type='Оқу справкасы', status='ready'),
                Document(user=user, doc_type='Өтінім', status='pending'),
                Document(user=user, doc_type='Студенттік куәландыру', status='ready'),
            ])
            self.stdout.write('Documents added')

        if not user.grades.exists():
            Grade.objects.bulk_create([
                Grade(user=user, subject='Ақпараттық жүйелер', score=85, status='Өтті'),
                Grade(user=user, subject='Жасанды интеллект', score=92, status='Өтті'),
                Grade(user=user, subject='Веб-технологиялар', score=78, status='Өтті'),
                Grade(user=user, subject='Базалық деректер', score=None, exam_status='Күтілуде', status='Оқуда'),
            ])
            self.stdout.write('Grades added')

        if not user.notifications.exists():
            Notification.objects.bulk_create([
                Notification(user=user, title='Справка дайын', message='Оқу справкасыңыз дайын. Жүктеу бөлімінен алуға болады.'),
                Notification(user=user, title='Емтихан кестесі', message='6 семестрдің емтихан кестесі жарияланды.'),
                Notification(user=user, title='Жаңалық', message='Жазғы практика орналастыру басталды.'),
            ])
            self.stdout.write('Notifications added')

        self.stdout.write(self.style.SUCCESS('Demo data ready!'))
