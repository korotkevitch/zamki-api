from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APITestCase
from service.models import Service
from service.api.serializers import ServiceSerializer, ServiceImageSerializer
from service import models


class ServiceApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='iko', password='iko@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko', 'password': 'iko@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.service = models.Service.objects.create(service="service_1", description="description_1")

    def test_service_create_is_superuser(self):
        data = {
            'service': "service_2",
            'description': 'description_2'}
        response = self.client.post(reverse('service-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_service_create_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            'service': "service_2",
            'description': 'description_2'}
        response = self.client.post(reverse('service-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_create_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            'service': "service_2",
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
        self.assertEqual(models.Service.objects.get().service, 'service_1')

    def test_service_detail_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('service-detail', args=(self.service.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().service, 'service_1')

    def test_service_detail_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('service-detail', args=(self.service.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().service, 'service_1')

    def test_service_update_is_superuser(self):
        data = {
            "service": "my_service",
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
            "service": "my_service",
            "description": "my_description"
        }
        response = self.client.put(reverse('service-detail', args=(self.service.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_update_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            "service": "my_service",
            "description": "my_description"
        }
        response = self.client.put(reverse('service-detail', args=(self.service.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)