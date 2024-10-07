from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class ContactInfo(models.Model):
    """
    Модель для хранения контактной информации звена сети.
    """
    email = models.EmailField("Email", unique=True)
    country = models.CharField("Страна", max_length=100)
    city = models.CharField("Город", max_length=100)
    street = models.CharField("Улица", max_length=100)
    house_number = models.CharField("Номер дома", max_length=10)

    def __str__(self):
        return f"{self.email} | {self.city}, {self.street} {self.house_number}"


class NetworkNode(models.Model):
    """
    Модель звена сети по продаже электроники.
    """

    NODE_TYPES = (
        ('factory', 'Завод'),
        ('retail', 'Розничная сеть'),
        ('entrepreneur', 'Индивидуальный предприниматель'),
    )

    name = models.CharField("Название", max_length=255)
    node_type = models.CharField("Тип звена", max_length=20, choices=NODE_TYPES)
    contact_info = models.OneToOneField(
        ContactInfo,
        verbose_name="Контактная информация",
        on_delete=models.CASCADE,
        related_name='network_node'
    )
    supplier = models.ForeignKey(
        'self',
        verbose_name="Поставщик",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients'
    )
    debt = models.DecimalField(
        "Задолженность перед поставщиком",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def __str__(self):
        return f"{self.get_node_type_display()} - {self.name}"

    def clean(self):
        """
        Дополнительная валидация модели.
        """
        from django.core.exceptions import ValidationError

        # Завод не может иметь поставщика
        if self.node_type == 'factory' and self.supplier is not None:
            raise ValidationError("Завод не может иметь поставщика.")

        # Проверка циклических ссылок
        supplier = self.supplier
        while supplier is not None:
            if supplier == self:
                raise ValidationError("Циклическая ссылка в поставщиках.")
            supplier = supplier.supplier

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"


class Product(models.Model):
    """
    Модель продукта, реализуемого звеном сети.
    """
    name = models.CharField("Название", max_length=255)
    model = models.CharField("Модель", max_length=255)
    release_date = models.DateField("Дата выхода на рынок")
    network_node = models.ForeignKey(
        NetworkNode,
        verbose_name="Звено сети",
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
