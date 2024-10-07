from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer


class IsActiveUser(permissions.BasePermission):
    """
    Разрешение доступа только для активных сотрудников.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели NetworkNode.
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['contact_info__country']
    search_fields = ['name', 'contact_info__city']

    def get_queryset(self):
        """
        Переопределение queryset для оптимизации запросов.
        """
        return NetworkNode.objects.select_related('contact_info', 'supplier').prefetch_related('products')
