# from authentication.serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError

from .models import User, Contributor, Project, Issue, Comment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Email déjà utilisé.')
        return value

    def validate_password(self, value):
        """Hashes password."""
        if len(value) < 8:
            raise ValidationError('Votre mot de passe doit contenir au moins 8 caractères')
        return make_password(value)

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        if first_name.isalnum() and last_name.isalnum():
            data['username'] = email
            return data
        else:
            raise ValidationError('First and last names must be only numeric.')


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['project_id', 'user_id', 'permission', 'role', 'id']


class ProjectSerializer(ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ('title', 'description', 'type', 'users',)




class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ('title', 'description', 'tag', 'priority', 'status', 'assignee_user', 'created_time',)



class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('description', 'created_time',)

