from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'capacity': {'required': True},
            'price': {'required': True},
            'image': {'required': True},
        }
