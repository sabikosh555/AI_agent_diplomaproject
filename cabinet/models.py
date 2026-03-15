"""
Cabinet app - models for personal cabinet
"""
from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    """Профиль студента - расширение User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField('Студенттік ID', max_length=20, blank=True)
    course = models.PositiveSmallIntegerField('Курс', default=3)
    faculty = models.CharField('Факультет', max_length=100, default='Ақпараттық технологиялар')
    specialty = models.CharField('Мамандық', max_length=100, default='Ақпараттық жүйелер')

    class Meta:
        verbose_name = 'Студент профилі'
        verbose_name_plural = 'Студент профильдері'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Document(models.Model):
    """Документ студента."""
    STATUS_CHOICES = [
        ('pending', 'Қаралуда'),
        ('ready', 'Дайын'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField('Құжат түрі', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = 'Құжат'
        verbose_name_plural = 'Құжаттар'


class Grade(models.Model):
    """Оценка по предмету."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    subject = models.CharField('Пән', max_length=100)
    score = models.PositiveSmallIntegerField('Баға', null=True, blank=True)
    exam_status = models.CharField('Емтихан', max_length=50, blank=True)
    status = models.CharField('Мәртебе', max_length=20, default='Өтті')

    class Meta:
        verbose_name = 'Баға'
        verbose_name_plural = 'Бағалар'


class Schedule(models.Model):
    """Расписание занятий."""
    DAYS = [
        (1, 'Дүйсенбі'), (2, 'Сейсенбі'), (3, 'Сәрсенбі'),
        (4, 'Бейсенбі'), (5, 'Жұма'),
    ]
    day = models.PositiveSmallIntegerField(choices=DAYS)
    time_start = models.TimeField('Басталу')
    time_end = models.TimeField('Аяқталу')
    subject = models.CharField('Пән', max_length=100)
    course = models.PositiveSmallIntegerField('Курс', default=3)

    class Meta:
        verbose_name = 'Кесте'
        verbose_name_plural = 'Кестелер'
        ordering = ['day', 'time_start']


class Notification(models.Model):
    """Уведомление."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField('Тақырып', max_length=200)
    message = models.TextField('Хабарлама')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Хабарлама'
        verbose_name_plural = 'Хабарламалар'


class ProblemSolution(models.Model):
    """
    Студенттердің жиі кездесетін мәселелері мен шешімдері.
    Админ қосқан шешімдер AI көмекшіге контекст ретінде беріледі.
    """
    topic = models.CharField('Тақырып / Мәселе', max_length=200, help_text='Қысқаша сипаттама')
    keywords = models.CharField(
        'Кілт сөздер',
        max_length=300,
        blank=True,
        help_text='Студент сұрағанда ізделетін сөздер (мысалы: справка, құжат, кесте)'
    )
    solution = models.TextField('Шешім / Жауап', help_text='Мәселені қалай шешу керек')
    is_active = models.BooleanField('Белсенді', default=True)
    order = models.PositiveSmallIntegerField('Рет', default=0, help_text='Кіші сан — бірінші')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Мәселе шешімі'
        verbose_name_plural = 'Мәселе шешімдері'
        ordering = ['order', 'topic']

    def __str__(self):
        return self.topic
