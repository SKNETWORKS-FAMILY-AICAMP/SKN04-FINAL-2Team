from rest_framework import serializers
from .models import CustomUser

# 사용자 등록 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# 사용자 프로필 시리얼라이저
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_active', 'is_staff', 'is_host', 'is_superuser')

# 사용자 업데이트 시리얼라이저
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)