from django.test import TestCase
from electronics_network.models import NetworkNode, ContactInfo


class NetworkNodeModelTest(TestCase):

    def setUp(self):
        # Создаем контактную информацию для объектов сети
        self.contact_info_1 = ContactInfo.objects.create(
            email="test1@example.com",
            country="Russia",
            city="Moscow",
            street="Lenina",
            house_number="10"
        )
        self.contact_info_2 = ContactInfo.objects.create(
            email="test2@example.com",
            country="Russia",
            city="Saint Petersburg",
            street="Nevsky",
            house_number="15"
        )

        # Создаем завод (уровень 0)
        self.factory = NetworkNode.objects.create(
            name="Factory 1",
            node_type="factory",
            contact_info=self.contact_info_1,
            debt=0
        )

        # Создаем розничную сеть (уровень 1)
        self.retail_network = NetworkNode.objects.create(
            name="Retail Network 1",
            node_type="retail",
            contact_info=self.contact_info_2,
            supplier=self.factory,
            debt=5000.25
        )

    def test_factory_creation(self):
        # Проверка создания завода
        self.assertEqual(self.factory.name, "Factory 1")
        self.assertEqual(self.factory.debt, 0)

    def test_retail_network_creation(self):
        # Проверка создания розничной сети и связи с поставщиком
        self.assertEqual(self.retail_network.name, "Retail Network 1")
        self.assertEqual(self.retail_network.supplier, self.factory)
        self.assertEqual(self.retail_network.debt, 5000.25)
