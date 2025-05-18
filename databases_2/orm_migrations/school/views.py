from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    students = Student.objects.order_by('group').prefetch_related('teachers')
    return render(request, 'school/students_list.html', {'object_list': students})


class StudentListView(ListView):
    model = Student
    ordering = 'group'
    template_name = 'school/students_list.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('teachers')
