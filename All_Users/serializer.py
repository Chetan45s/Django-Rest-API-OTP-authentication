from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from All_Users.models import User, Profile
# User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('Phone','password','First_Name','Last_Name',)
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','Phone',)

class LoginUserSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(Phone=phone).exists():
                user = authenticate(request=self.context.get('request'),Phone=phone, password=password)
            else:
                msg = {'detail': 'Phone number is not registered','register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "Phone" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'Phone',
            'First_Name',
            'Last_Name',
            'video',
            'is_video_validated',
            'bio',
            'profile_pic',
            'is_private',
        )

class ProfilePrivateSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'Phone',
            'First_Name',
            'Last_Name',
            'is_video_validated',
            'bio',
            'profile_pic',
            'is_private',
        )