# Работа с базой (отображение списка моделей)

## Задание

Необходимо сделать онлайн библиотеку с каталогом книг. Библиотека должна состоять из двух страниц:
* `/books` - отображение списка книг
* `/books/2018-01-02/` - отображение списка книг за дату 2018-01-02 (год, месяц, день)

Книга имеет три параметра:
* Название
* Автор
* Дата публикации (pub_date)

Так же на странице `/books/<pub_date>/` сделать возможность пагинации на страницу с книгами предыдущей даты и следующей даты.
Например: в библиотеке имеется 4 книги: одна за пятое число условного месяца, вторая за третье число того же месяца, 
третья за десятое и последняя за одиннадцатое. На странице `/books` отображаем все эти книги. А на странице `/books/2018-09-05/`
отображаем первую книгу, и ссылки на страницу с книгами за предыдущую дату (2018-09-03) и следующую дату (2018-09-10).

## Добавления по проекту

При вводе `/books/2018-09-05/` даты большей или меньшей дат книг, отображается книга с большей или меньшей датой.

![Каталог со всеми книгами](res/catalog_1.png)

![Каталог с книгами выбранной даты публикования](res/catalog_2.png)
