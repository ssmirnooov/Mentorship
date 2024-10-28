from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "testuser@example.com"
        }
        self.mentor = User.objects.create_user(
            username="mentor",
            password="mentorpassword123",
            email="mentor@example.com"
        )
        self.user = User.objects.create_user(
            **self.user_data
        )
        self.user.mentor = self.mentor
        self.user.save()
        
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_registration(self):
        url = reverse('registration')
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # Два тестовых пользователя + новый

    def test_login(self):
        url = reverse('login')
        data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_list_accessible(self):
        url = reverse('user_list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_user_detail(self):
        url = reverse('user_detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data["username"])
        self.assertEqual(response.data['mentor'], self.mentor.username)

    def test_user_update_self_only(self):
        url = reverse('user_detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        data = {
            "username": "updateduser",
            "phone": "+123456789"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.phone, "+123456789")

    def test_mentor_access_to_mentees(self):
        url = reverse('user_detail', kwargs={'pk': self.mentor.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)
        self.assertIn(self.user_data["username"], [mentee["username"] for mentee in response.data.get("mentees", [])])
