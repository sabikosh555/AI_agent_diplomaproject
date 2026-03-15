"""
Staff пайдаланушысын құру
python manage.py create_staff
python manage.py create_staff --username staff --password staff123
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Staff пайдаланушысын құрады'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Пайдаланушы аты')
        parser.add_argument('--password', default='admin123', help='Құпия сөз')
        parser.add_argument('--email', default='admin@university.kz', help='Пошта')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Staff user created: {username} / {password}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Staff user updated: {username} / {password}'))
