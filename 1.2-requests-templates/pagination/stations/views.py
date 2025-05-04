import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # Читаем данные из CSV-файла
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        stations_list = list(reader)

    # Создаем пагинатор
    paginator = Paginator(stations_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Получаем "усеченный" диапазон страниц для пагинации
    elided_page_range = paginator.get_elided_page_range(
        number=page_number,
        on_each_side=3,
        on_ends=1
    )

    context = {
        'bus_stations': page_obj.object_list,    # Список станций на текущей странице
        'page_obj': page_obj,                    # Объект страницы
        'elided_page_range': elided_page_range,  # Диапазон страниц для отображения
    }
    return render(request, 'stations/index.html', context)
