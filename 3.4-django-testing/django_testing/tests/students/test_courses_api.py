import pytest
from model_bakery import baker
from django.urls import reverse
from students.models import Course, Student


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make(Student, **kwargs)
    return factory

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    """проверка получения первого курса (retrieve-логика)"""
    # Arrange
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    """проверка получения списка курсов (list-логика)"""
    courses = course_factory(_quantity=3)
    url = reverse('courses-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3
    for i, course in enumerate(courses):
        assert response.data[i]['id'] == course.id
        assert response.data[i]['name'] == course.name

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    """проверка фильтрации списка курсов по id"""
    courses = course_factory(_quantity=3)
    url = reverse('courses-list')

    response = api_client.get(url, {'id': courses[0].id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == courses[0].id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    """проверка фильтрации списка курсов по name"""
    course = course_factory(name='Спец-курс')
    course_factory(name='Начальный курс')
    url = reverse('courses-list')

    response = api_client.get(url, {'name': 'Спец-курс'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Спец-курс'

@pytest.mark.django_db
def test_create_course(api_client):
    """тест успешного создания курса"""
    url = reverse('courses-list')
    data = {'name': 'Созданный курс'}

    response = api_client.post(url, data)

    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'Созданный курс'

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """тест успешного обновления курса"""
    course = course_factory(name='Старое название')
    url = reverse('courses-detail', args=[course.id])
    data = {'name': 'Новое название'}

    response = api_client.put(url, data)

    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Новое название'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """тест успешного удаления курса"""
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])

    response = api_client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == 0
