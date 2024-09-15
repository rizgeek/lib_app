from django.contrib.auth.models import User, Group
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    group = serializers.ChoiceField(choices=['librarian', 'student'], required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'group']
    
    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, data) :
        name = data['name']
        email = data['email']
        password = data['password']
        group_name = data['group']

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )

        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        return user