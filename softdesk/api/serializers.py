# from authentication.serializers import UserSerializer


from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField, HiddenField, CurrentUserDefault, IntegerField

from .models import User, Contributor, Project, Issue, Comment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Email is alrealdy used')
        return value

    def validate_password(self, value):
        # """ Constraint on password"""
        # if len(value) < 8:
        #     raise ValidationError('Votre mot de passe doit contenir au moins 8 caractères')
        return make_password(value)

    def validate(self, data):
        """ Constraint on first name and last name. Use email as username """        
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        if first_name.isalnum() and last_name.isalnum():
            data['username'] = email
            return data
        else:
            raise ValidationError('Name and last name must contain only letter or numbers')


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user_id', 'type']
        read_only = ['id', 'author_user_id']



class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'role']
        read_only = ['id', 'permission']        
        # fields = "__all__"        


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']
        read_only = ['id', 'author_user_id']


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'assignee_user_id']
        read_only = ['id', 'author_user_id']        


class IssueDetailSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'priority', 'project_id', 'description', 'tag', 'status', 'author_user_id', 'assignee_user']
        read_only = ['id', 'author_user_id']


class CommentListSerializer(ModelSerializer): 
    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'description', 'author_user_id', 'created_time']
        read_only = ['id', 'author_user_id', 'issue_id', 'created_time']


class CommentDetailSerializer(ModelSerializer): 
    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'description', 'author_user_id', 'created_time']
        read_only = ['id', 'author_user_id', 'issue_id', 'created_time']
        
        
