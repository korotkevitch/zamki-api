from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from articles.models import Article
from services.models import Service
from articles import models
import os
from PIL import Image
import tempfile


class ArticleApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='iko', password='iko@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko', 'password': 'iko@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.service = models.Service.objects.create(name="name_1", description="description_1")
        self.article = models.Article.objects.create(
            title="title_1",
            related_service=self.service,
            storyline="storyline_1",
            text="text_1",
            user=self.user,
            active=True
        )

    def test_article_create_is_superuser(self):
        data = {
            "title": "title_2",
            "related_service": self.service.id,
            "storyline": "storyline_2",
            "text": "text_2",
            "user": self.user.id,
            "active": True,
            "avg_rating": "4",
            "number_rating": "1"
        }
        response = self.client.post(reverse('article-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_article_create_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "title": "title_2",
            "related_service": self.service.id,
            "storyline": "storyline_2",
            "text": "text_2",
            "user": self.user.id,
            "active": True,
            "avg_rating": "4",
            "number_rating": "1"
        }
        response = self.client.post(reverse('article-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_article_create_is_unauthorized(self):
        data = {
            "title": "title_2",
            "related_service": self.service.id,
            "storyline": "storyline_2",
            "text": "text_2",
            "active": True,
            "avg_rating": "4",
            "number_rating": "1",
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('article-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_article_list_is_superuser(self):
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_list_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_list_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_detail_is_superuser(self):
        response = self.client.get(reverse('article-detail', args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Service.objects.count(), 1)
        self.assertEqual(models.Service.objects.get().name, 'name_1')

    def test_article_detail_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('article-detail', args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Article.objects.count(), 1)
        self.assertEqual(models.Article.objects.get().title, 'title_1')

    def test_article_detail_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('article-detail', args=(self.article.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Article.objects.count(), 1)
        self.assertEqual(models.Article.objects.get().title, 'title_1')

    """ Article was created by superuser in setUp. """
    def test_article_update_is_superuser(self):
        data = {
            "title": "title_updated",
            "text": "text_updated",
            "user": self.user.id,
            "related_service": self.service.id
        }
        response = self.client.put(reverse('article-detail', args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """ User is not owner. Owner is superuser """
    def test_article_update_is_user(self):
        self.user = User.objects.create_user(username='iko2', password='iko2@123.com')
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'iko2', 'password': 'iko2@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "title": "title_updated",
            "text": "text_updated",
            "user": self.user.id,
            "related_service": self.service.id
        }
        response = self.client.put(reverse('article-detail', args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_update_is_unauthorized(self):
        self.client.force_authenticate(user=None)
        data = {
            "title": "title_updated",
            "text": "text_updated",
            "user": self.user.id,
            "related_service": self.service.id
        }
        response = self.client.put(reverse('article-detail', args=(self.article.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def detail_url(article_id):
    """Create and return an article detail URL."""
    return reverse('article-detail', args=[article_id])

def image_upload_url(article_id):
    """Create and return an image upload URL."""
    return reverse('article-upload-image', args=[article_id])


class ImageUploadTests(APITestCase):
    """Tests for the image upload API."""

    def setUp(self):
        """ Owner is 'user_new' created in 'create_article'. """
        self.user = User.objects.create_user(username="user_new", password="user_new@123.com")
        response = self.client.post(reverse('token_obtain_pair'), data={'username': 'user_new', 'password': 'user_new@123.com'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.client.force_authenticate(self.user)
        self.service = models.Service.objects.create(name="name_1", description="description_1")
        self.article = models.Article.objects.create(
            title="title_1",
            related_service=self.service,
            storyline="storyline_1",
            text="text_1",
            user=self.user,
            active=True
        )

    def tearDown(self):
        self.article.image.delete()

    def test_upload_image(self):
        """Test uploading an image to an article."""
        url = image_upload_url(self.article.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.article.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.article.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.article.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
