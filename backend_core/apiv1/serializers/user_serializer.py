from rest_framework.serializers import ModelSerializer
from users.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
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
        )
