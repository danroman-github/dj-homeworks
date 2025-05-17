from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'  # Параметр сортировки по классу

    # Получаем всех учеников с предварительной загрузкой учителей для оптимизации запросов
    students = Student.objects.order_by(ordering).prefetch_related('teachers')

    context = {
        'object_list': students,  # Передаем список учеников в контекст
    }

    return render(request, template, context)
