from rest_framework import status
from model_bakery import baker
import pytest
from store.models import Collection, Product


# Fixtures
@pytest.fixture
def create_collection(api_client):
	def do_create_collection(collection):
		return api_client.post('/store/collections/', collection)
	return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:

	def test_if_user_is_anonymouse_returns_401(self, create_collection):
		response = create_collection({'title': 'a'})

		assert response.status_code == status.HTTP_401_UNAUTHORIZED


	def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate_user):
		authenticate_user()

		response = create_collection({'title': 'a'})

		assert response.status_code == status.HTTP_403_FORBIDDEN


	def test_if_data_is_invalid_returns_400(self, create_collection, authenticate_user):
		authenticate_user(is_staff=True)

		response = create_collection({'title': ''})

		assert response.status_code == status.HTTP_400_BAD_REQUEST
		assert response.data['title'] is not None


	def test_if_data_is_valid_returns_201(self, create_collection, authenticate_user):
		authenticate_user(is_staff=True)

		response = create_collection({'title': 'a'})
		
		assert response.status_code == status.HTTP_201_CREATED
		assert response.data['id'] > 0



@pytest.mark.django_db
class TestRetrieveCollection:

	def test_if_collection_exists_returns_200(self, api_client):
		collection = baker.make(Collection)

		response = api_client.get(f'/store/collections/{collection.id}/')

		assert response.status_code == status.HTTP_200_OK
		assert response.data == {'id': collection.id, 'title': collection.title, 'products_count': 0}


	def test_if_collection_does_not_exist_returns_404(self, api_client):
		response = api_client.get(f'/store/collections/0/')
		assert response.status_code == status.HTTP_404_NOT_FOUND


	def test_retrieve_all_collections(self, api_client):
		response = api_client.get('/store/collections/')

		assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestUpdateCollection:

	def test_if_user_is_anonymouse_returns_401(self, api_client, authenticate_user):
		collection = baker.make(Collection)

		response = api_client.put(f'/store/collections/{collection.id}/', data={'title': 'a'})

		assert response.status_code == status.HTTP_401_UNAUTHORIZED


	def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
		collection = baker.make(Collection)
		authenticate_user()

		response = api_client.put(f'/store/collections/{collection.id}/', data={'title': 'a'})

		assert response.status_code == status.HTTP_403_FORBIDDEN



	def test_if_data_valid_returns_200(self, api_client, authenticate_user):
		collection = baker.make(Collection)
		authenticate_user(is_staff=True)

		response = api_client.put(f'/store/collections/{collection.id}/', data={'title': 'a'})

		assert response.status_code == status.HTTP_200_OK

	
	def test_if_data_invalid_returns_400(self, api_client, authenticate_user):
		collection = baker.make(Collection)
		authenticate_user(is_staff=True)

		response = api_client.put(f'/store/collections/{collection.id}/', data={'title': ''})

		assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteCollection:

	def test_anonymouse_user_returns_401(self, api_client):
		collection = baker.make(Collection)

		response = api_client.delete(f'/store/collections/{collection.id}/')

		assert response.status_code == status.HTTP_401_UNAUTHORIZED


	def test_if_user_is_not_admin(self, api_client, authenticate_user):
		authenticate_user()
		collection = baker.make(Collection)

		response = api_client.delete(f'/store/collections/{collection.id}/')

		assert response.status_code == status.HTTP_403_FORBIDDEN



	def test_collection_has_products_returns_405(self, api_client, authenticate_user):
		authenticate_user(is_staff=True)
		collection = baker.make(Collection)
		products = baker.make(Product, collection=collection, _quantity=5)

		response = api_client.delete(f'/store/collections/{collection.id}/')

		assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

	
	def test_empty_collection_204(self, api_client, authenticate_user):
		authenticate_user(is_staff=True)
		collection = baker.make(Collection)

		response = api_client.delete(f'/store/collections/{collection.id}/')

		assert response.status_code == status.HTTP_204_NO_CONTENT
	