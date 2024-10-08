from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from electronics_network.models import NetworkNode, ContactInfo


class NetworkNodeViewSetTest(APITestCase):

    def setUp(self):
        # Создаем активного пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass', is_active=True)
        self.client.login(username='testuser', password='testpass')

        # Создаем контактную информацию и объекты сети для тестирования
        self.contact_info_1 = ContactInfo.objects.create(
            email="contact1@example.com",
            country="Russia",
            city="Moscow",
            street="Red Square",
            house_number="1"
        )
        self.contact_info_2 = ContactInfo.objects.create(
            email="contact2@example.com",
            country="USA",
            city="New York",
            street="5th Avenue",
            house_number="101"
        )

        self.network_node_1 = NetworkNode.objects.create(
            name="Factory 1",
            node_type="factory",
            contact_info=self.contact_info_1,
            debt=1000.50
        )

        self.network_node_2 = NetworkNode.objects.create(
            name="Retail Network 1",
            node_type="retail",
            contact_info=self.contact_info_2,
            supplier=self.network_node_1,
            debt=5000.25
        )

    def test_create_network_node(self):
        # Тестирование создания нового объекта через API
        url = reverse('networknode-list')
        data = {
            'name': 'New Factory',
            'node_type': 'factory',
            'contact_info': {
                'email': 'newcontact@example.com',
                'country': 'France',
                'city': 'Paris',
                'street': 'Champs-Élysées',
                'house_number': '100'
            },
            'debt': 0.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'New Factory')

    def test_get_network_nodes(self):
        # Тестирование получения списка объектов
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_country(self):
        # Тестирование фильтрации по стране
        url = reverse('networknode-list')
        response = self.client.get(url, {'contact_info__country': 'USA'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Retail Network 1')

    def test_delete_network_node(self):
        # Тестирование удаления объекта
        url = reverse('networknode-detail', args=[self.network_node_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_active_user_access(self):
        # Тестирование доступа только для активных пользователей
        self.client.logout()
        url = reverse('networknode-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
