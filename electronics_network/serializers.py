from rest_framework import serializers
from .models import NetworkNode, ContactInfo, Product


class ContactInfoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ContactInfo.
    """
    class Meta:
        model = ContactInfo
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkNode.
    """
    contact_info = ContactInfoSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = NetworkNode
        exclude = ('debt',)  # Запрет обновления через API поля "Задолженность перед поставщиком"

    def create(self, validated_data):
        """
        Переопределение метода создания объекта.
        """
        contact_data = validated_data.pop('contact_info')
        contact_info = ContactInfo.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact_info=contact_info, **validated_data)
        return network_node

    def update(self, instance, validated_data):
        """
        Переопределение метода обновления объекта.
        """
        contact_data = validated_data.pop('contact_info', None)
        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact_info, attr, value)
            instance.contact_info.save()
        for attr, value in validated_data.items():
            if attr != 'debt':  # Запрет обновления поля "Задолженность перед поставщиком"
                setattr(instance, attr, value)
        instance.save()
        return instance
