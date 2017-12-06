from rest_framework.serializers import ModelSerializer
from users.models import User
from ..utils import get_uuid
from datetime import datetime
from allauth.account.adapter import get_adapter

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'password',
            'last_login',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'role',
            'hoome_id',
            'uuid'
        )
        read_only_fields = (
            'uuid',
            'hoome_id',
            'date_joined',
            'last_login',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['date_joined'] = datetime.now()
        validated_data['last_login'] = datetime.now()
        validated_data['uuid'] = get_uuid(model=self.Meta.model)
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['id'] = getattr(instance, 'id')
        return super(UserSerializer, self).update(instance, validated_data)

