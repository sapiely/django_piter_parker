import json
import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from django.core.management import call_command
from django.core.management.commands import testserver

from sales.models import Company, Product


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'data.json')


@pytest.mark.django_db
def test_user_create(db, django_db_setup):
    User.objects.create_user('Sam Porter Bridges', "sam@bridges.com", 'kojima-genius')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_product_create(api_client):
    url = reverse('category-list')
    category_body = {'name': 'Sample category'}
    response = api_client.post(url, category_body, format='json')

    category_response_body = json.loads(response.content)
    assert response.status_code == 201
    assert category_response_body.get('name') == 'Sample category'

    url = reverse('product-list')

    product_body = {"name": "Portal Gun", "category": category_response_body.get('id')}
    response = api_client.post(url, product_body, format='json')

    product_response_body = json.loads(response.content)

    assert Product.objects.count() != 1
    assert response.status_code == 201
    assert product_response_body.get('name') == 'Portal Gun'
    assert product_response_body.get('category_id') == category_response_body.get('id')
    assert product_response_body.get('category_name') == 'Sample category'


@pytest.mark.django_db
def test_product_view(api_client):
    url = reverse('product-list')
    response = api_client.get(url)
    body = json.loads(response.content)

    assert len(body) == 10
    assert {"id": 1,
            "name": "Iphone",
            "category_id": 1,
            "category_name": "Technology"
            } in body
    assert {"id": 7,
            "name": "Steam",
            "category_id": 3,
            "category_name": "Something else"
            } in body


@pytest.mark.django_db
def test_company_detail_view(api_client):
    url = reverse('organization-detail', kwargs={'id': 1})
    response = api_client.get(url)
    body = json.loads(response.content)

    assert len(body) == 1
    assert body[0]['id'] == 1
    assert body[0]['district']['id'] == 1
    assert len(body[0]['products']) == 5


@pytest.mark.django_db
def test_company_list_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url)
    body = json.loads(response.content)

    assert len(body) == 2


@pytest.mark.django_db
def test_company_max_price_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'price': 'max'})
    body = json.loads(response.content)

    assert body[0]['products']['price'] == '432.00'
    assert body[1]['products']['price'] == '12.00'


@pytest.mark.django_db
def test_company_min_price_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'price': 'min'})
    body = json.loads(response.content)

    assert body[0]['products']['price'] == '8.00'
    assert body[1]['products']['price'] == '12.00'


@pytest.mark.django_db
def test_company_category_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'category': 'Technology'})
    body = json.loads(response.content)

    assert len(body[0]['products']) == 3
    assert len(body[1]['products']) == 1

    for company in body:
        for product in company['products']:
            assert product['category']['name'] == 'Technology'


@pytest.mark.django_db
def test_company_district_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'district_id': 1})
    body = json.loads(response.content)

    assert len(body) == 1
    assert body[0]['district'][0]['id'] == 1


@pytest.mark.django_db
def test_company_category_and_max_price_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'category': 'Something else', 'price': 'max'})
    body = json.loads(response.content)

    assert body[0]['products'] != list
    assert body[1]['products'] is None

    assert body[0]['products']['price'] == '123.00'
    assert body[0]['products']['category']['name'] == 'Something else'


@pytest.mark.django_db
def test_company_category_and_district_and_max_price_view(api_client):
    url = reverse('organization-list')
    response = api_client.get(url, {'category': 'Something else',
                                    'price': 'max',
                                    'district_id': 1})
    body = json.loads(response.content)

    assert body[0]['products'] != list
    assert len(body) == 1

    assert body[0]['products']['price'] == '123.00'
    assert body[0]['products']['category']['name'] == 'Something else'
    assert body[0]['district'][0]['id'] == 1
