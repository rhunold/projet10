from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import User, Contributor, Project, Issue, Comment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Email is alrealdy used.')
        return value

    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        """ Constraint on first name and last name. Use email as username """
        email = data['email']
        data['username'] = email
        return data


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user_id', 'project_id', 'role', 'permission']
        read_only = ['id', 'permission']


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user_id', 'type']
        read_only = ['id', 'author_user_id']


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only = ['id', 'author_user_id']


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'assignee_user_id']
        read_only = ['id', 'author_user_id']


class IssueDetailSerializer(ModelSerializer):
    class Meta:
        model = Issue
        exclude = ['project', 'author_user']
        read_only = ['id', 'author_user_id']


class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'author_user': {'required': False}, 'issue' : {'required': False}}
        read_only = ['id', 'author_user', 'issue', 'created_time']     


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created_time']
        read_only = ['id', 'author_user_id', 'issue_id', 'created_time']

