from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from services.models import Service
from services import models
import os
from PIL import Image
import tempfile


class ServiceApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='iko', password='iko@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko', 'password': 'iko@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.service = models.Service.objects.create(name="name_1", description="description_1")

    def test_service_create_is_superuser(self):
        data = {
            'name': "name_2",
            'description': 'description_2'}
        response = self.client.post(reverse('service-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_service_create_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'name': "name_2",
            'description': 'description_2'}
        response = self.client.post(reverse('service-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_create_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            'name': "name_2",
            'description': 'description_2'}
        response = self.client.post(reverse('service-list'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_list_is_superuser(self):
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_service_list_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_service_list_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('service-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_service_detail_is_superuser(self):
        response = self.client.get(reverse('service-detail', args=(self.service.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().name, 'name_1')

    def test_service_detail_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('service-detail', args=(self.service.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().name, 'name_1')

    def test_service_detail_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('service-detail', args=(self.service.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().name, 'name_1')

    def test_service_update_is_superuser(self):
        data = {
            "name": "my_name",
            "description": "my_description"
        }
        response = self.client.put(reverse('service-detail', args=(self.service.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_service_update_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "name": "my_name",
            "description": "my_description"
        }
        response = self.client.put(reverse('service-detail', args=(self.service.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_update_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            "name": "my_name",
            "description": "my_description"
        }
        response = self.client.put(reverse('service-detail', args=(self.service.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def detail_url(service_id):
    """Create and return a service detail URL."""
    return reverse('service-detail', args=[service_id])

def image_upload_url(service_id):
    """Create and return an image upload URL."""
    return reverse('service-upload-image', args=[service_id])

def create_service(**params):
    """Create and return a sample service."""
    defaults = {
        'name': 'Sample service title',
        'description': 'sample_description',
    }
    defaults.update(params)

    service = Service.objects.create(**defaults)
    return service


class ImageUploadTests(APITestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.user = User.objects.create_superuser(username='iko', password='iko@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko', 'password': 'iko@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.force_authenticate(self.user)
        self.service = create_service()

    def tearDown(self):
        self.service.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a recipe."""
        url = image_upload_url(self.service.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.service.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.service.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.service.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
