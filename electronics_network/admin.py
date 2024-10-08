from django.contrib import admin
from .models import NetworkNode, ContactInfo, Product


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """
    Административная панель для модели ContactInfo.
    """
    list_display = ('email', 'country', 'city', 'street', 'house_number')
    search_fields = ('email', 'city', 'street')


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """
    Административная панель для модели NetworkNode.
    """
    list_display = ('name', 'node_type', 'supplier', 'debt', 'created_at')
    list_filter = ('node_type', 'contact_info__city')
    search_fields = ('name', 'contact_info__city')
    readonly_fields = ('created_at',)
    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        """
        Функция для обнуления задолженности выбранных звеньев.
        """
        queryset.update(debt=0)
        self.message_user(request, "Задолженность успешно обнулена.")
    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def get_queryset(self, request):
        """
        Переопределение queryset для оптимизации запросов.
        """
        qs = super().get_queryset(request)
        return qs.select_related('contact_info', 'supplier')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Product.
    """
    list_display = ('name', 'model', 'release_date', 'network_node')
    list_filter = ('release_date',)
    search_fields = ('name', 'model')
