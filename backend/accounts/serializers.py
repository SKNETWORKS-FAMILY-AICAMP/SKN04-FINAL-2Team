from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        # 응답 형식을 통일
        return {
            'success': True,
            'token': {
                'access': data['access'],
                'refresh': data['refresh'],
            },
            'user': {
                'username': user.username,
                'id': user.id,
                'email': user.email,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff
            }
        }

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # 응답 형식을 통일
        return {
            'success': True,
            'token': {
                'access': data['access'],
                # refresh token은 보안상 새로 발급된 것을 반환하지 않음
            }
        }

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
        fields = ('email', 'is_active', 'is_staff', 'is_superuser')

# 사용자 업데이트 시리얼라이저
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
        
class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'is_staff')

    def update(self, instance, validated_data):
        instance.is_staff = True  # 직접 staff 권한 부여
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

