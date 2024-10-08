from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from electronics_network.models import NetworkNode, ContactInfo


class NetworkNodeAPITest(APITestCase):

    def setUp(self):
        # Создаем активного пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass', is_active=True)
        self.client.login(username='testuser', password='testpass')

        # Создаем контактную информацию и объекты сети
        self.contact_info = ContactInfo.objects.create(
            email="api_test@example.com",
            country="USA",
            city="New York",
            street="5th Avenue",
            house_number="101"
        )
        self.factory = NetworkNode.objects.create(
            name="API Test Factory",
            node_type="factory",
            contact_info=self.contact_info,
            debt=0
        )

    def test_active_user_access(self):
        # Проверка доступа к API активного пользователя
        response = self.client.get('/api/network-nodes/')
        self.assertEqual(response.status_code, 200)

    def test_filter_by_country(self):
        # Проверка фильтрации по стране
        response = self.client.get('/api/network-nodes/?contact_info__country=USA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'API Test Factory')
