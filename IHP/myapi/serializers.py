from rest_framework import serializers
from .models import CustomUser, SpamNumber, PhoneNumber, Name

class UserSerializer(serializers.ModelSerializer):
    # Serializer for creating a new user
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Password should be write-only

    def create(self, validated_data):
        # Create a new user with the provided data
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    # Serializer for CustomUser model
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'spam']  # Fields to include

class SpamNumberSerializer(serializers.ModelSerializer):
    # Serializer for SpamNumber model
    class Meta:
        model = SpamNumber
        fields = ['phone_number', 'spam_count']  # Fields to include

class NameSerializer(serializers.ModelSerializer):
    # Serializer for Name model
    class Meta:
        model = Name
        fields = ['name']  # Fields to include

class PhoneNumberSerializer(serializers.ModelSerializer):
    # Serializer for PhoneNumber model
    names = NameSerializer(many=True, read_only=True)  # Nested serializer for related names

    class Meta:
        model = PhoneNumber
        fields = ['number', 'names']  # Fields to include

    def create(self, validated_data):
        # Create a new phone number with the provided data
        names_data = validated_data.pop('names', [])  # Extract names data
        phone_number = PhoneNumber.objects.create(**validated_data)  # Create phone number object
        for name_data in names_data:
            Name.objects.create(phone_number=phone_number, **name_data)  # Create associated names
        return phone_number
