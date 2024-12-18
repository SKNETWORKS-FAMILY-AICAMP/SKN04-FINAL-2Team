from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import CustomUser

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.email = 'testuser@example.com'
        self.password = 'testpassword123'
        self.user = CustomUser.objects.create_user(email=self.email, password=self.password)

    def test_login_user(self):
        # 로그인 시도
        response = self.client.post(reverse('token_obtain_pair'), {'email': self.email, 'password': self.password})
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 토큰이 응답에 포함되어 있는지 확인
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_with_invalid_credentials(self):
        # 잘못된 자격 증명으로 로그인 시도
        response = self.client.post(reverse('token_obtain_pair'), {'email': self.email, 'password': 'wrongpassword'})
        
        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)