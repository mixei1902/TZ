from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from electronics_network.admin import NetworkNodeAdmin
from electronics_network.models import NetworkNode, ContactInfo


class NetworkNodeAdminTest(TestCase):

    def setUp(self):
        # Создаем объект админ-панели для тестов
        self.site = AdminSite()
        self.admin = NetworkNodeAdmin(NetworkNode, self.site)

        # Создаем тестового пользователя и RequestFactory
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

        # Создаем объекты модели для тестирования
        self.contact_info = ContactInfo.objects.create(
            email="admin_test@example.com",
            country="Russia",
            city="Moscow",
            street="Tverskaya",
            house_number="1"
        )
        self.factory_node = NetworkNode.objects.create(
            name="Test Factory",
            node_type="factory",
            contact_info=self.contact_info,
            debt=1000.50
        )

    def test_clear_debt(self):
        # Создаем фиктивный запрос
        request = self.factory.get('/admin/')
        request.user = self.user

        # Добавляем сессии к запросу
        middleware = SessionMiddleware(get_response=lambda r: None)
        middleware.process_request(request)
        request.session.save()

        # Добавляем поддержку FallbackStorage для сообщений
        setattr(request, '_messages', FallbackStorage(request))

        # Выбираем объекты, которые будем обновлять
        queryset = NetworkNode.objects.filter(id=self.factory_node.id)

        # Вызываем admin action для очистки задолженности
        self.admin.clear_debt(request, queryset)

        # Проверяем, что задолженность обнулилась
        updated_node = NetworkNode.objects.get(id=self.factory_node.id)
        self.assertEqual(updated_node.debt, 0)
