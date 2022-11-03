from rest_framework import status
from model_bakery import baker
import pytest
from store.models import Collection, Product


@pytest.mark.django_db
class TestRetrieveProduct:

	def test_products_list_returns_200(self, api_client):
		response = api_client.get('/store/products/')
		
		assert response.status_code == status.HTTP_200_OK

	
	def test_product_detail_returns_200(self, api_client):
		product = baker.make(Product)

		response = api_client.get(f'/store/products/{product.id}/')

		assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestCreateProduct:

	def test_anonymouse_user_returns_401(self, api_client):
		response = api_client.post('/store/products/')

		assert response.status_code == status.HTTP_401_UNAUTHORIZED


	def test_if_data_is_valid_returns_201(self, api_client, authenticate_user):
		authenticate_user(is_staff=True)

		response = api_client.post('/store/products/')

		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['id'] > 0


	def test_non_admin_user_returns_403(self, api_client, authenticate_user):
		authenticate_user()

		response = api_client.post('/store/products/')

		assert response.status_code == status.HTTP_403_FORBIDDEN
















