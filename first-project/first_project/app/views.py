import os

from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
from pathlib import Path
from django.conf import settings


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now().strftime('%H:%M:%S')
    home_url = reverse('home')
    return render(
        request,
        'app/current_time.html',
        {
            'current_time': current_time,
            'home_url': home_url
        }
    )


def workdir_view(request):
    home_url = reverse('home')
    project_dir = Path(__file__).resolve().parent.parent
    contents = []
    try:
        for item in Path(project_dir).iterdir():
            contents.append({
                'name': item.name,
                'type': 'directory' if item.is_dir() else 'file',
                'size': item.stat().st_size
            })
    except Exception as e:
        contents = [{'error': str(e)}]

    return render(
        request,
        'app/workdir.html',
        {
            'contents': contents,
            'home_url': home_url
        }
    )
