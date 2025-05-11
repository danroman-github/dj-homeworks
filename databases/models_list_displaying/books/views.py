from django.shortcuts import render, redirect
from books.models import Book
from datetime import datetime
from django.utils import timezone


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, template, context)


def books_by_date(request, pub_date):
    try:
        requested_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('books_by_date', pub_date=timezone.now().date().strftime('%Y-%m-%d'))

    min_date = Book.objects.all().order_by('pub_date').values('pub_date').first()
    min_date = min_date['pub_date'] if min_date else requested_date

    max_date = Book.objects.all().order_by('-pub_date').values('pub_date').first()
    max_date = max_date['pub_date'] if max_date else requested_date

    if requested_date < min_date:
        return redirect('books_by_date', pub_date=min_date.strftime('%Y-%m-%d'))

    if requested_date > max_date:
        return redirect('books_by_date', pub_date=max_date.strftime('%Y-%m-%d'))

    books = Book.objects.filter(pub_date=requested_date).order_by('name')

    prev_date = Book.objects.filter(
        pub_date__lt=requested_date
    ).order_by('-pub_date').values('pub_date').first()

    next_date = Book.objects.filter(
        pub_date__gt=requested_date
    ).order_by('pub_date').values('pub_date').first()

    context = {
        'books': books,
        'current_date': requested_date,
        'prev_date': prev_date['pub_date'] if prev_date else None,
        'next_date': next_date['pub_date'] if next_date else None,
        'is_min_date': requested_date == min_date,  # Флаг, что это минимальная дата
        'is_max_date': requested_date == max_date,  # Флаг, что это максимальная дата
        'requested_date': requested_date,  # Сохраняем оригинальную запрошенную дату
    }

    return render(request, 'books/books_by_date.html', context)
