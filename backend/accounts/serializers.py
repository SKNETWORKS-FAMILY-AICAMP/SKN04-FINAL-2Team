from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

# JWT 토큰 시리얼라이저 커스터마이징
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        # 토큰에 사용자 권한 정보 추가
        data.update({
            'is_host': user.is_host,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
            'username': user.username
        })
        
        return data

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
        
        


