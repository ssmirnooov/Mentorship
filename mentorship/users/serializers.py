from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    mentees = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)
    mentor = serializers.SlugRelatedField(slug_field='username', read_only=True)

    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'mentor', 'mentees']

