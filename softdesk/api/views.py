from rest_framework.viewsets import ModelViewSet

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsProjectContributor, IsProjectCreator, IsObjectAuthor

from rest_framework.exceptions import APIException, ValidationError

from .models import Project, Contributor, Issue, Comment, User
from .serializers import (
    UserSerializer, ContributorSerializer,
    ProjectListSerializer, ProjectDetailSerializer,
    IssueListSerializer, IssueDetailSerializer,
    CommentListSerializer, CommentDetailSerializer)


class SignUpView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsObjectAuthor]

    def get_queryset(self):
        user = self.request.user.id

        user_projects = [contrib.project_id for contrib in Contributor.objects.filter(user=user)]
        queryset = Project.objects.filter(id__in=user_projects)
        return queryset

    def perform_create(self, serializer):
        """ Create a Project and generate a Contributor with the user.request as Creator """
        user = self.request.user
        project = serializer.save(author_user=user)
        Contributor.objects.create(user=user, project=project, permission='CREATOR')


class ContributorsViewset(ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectCreator]

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, id=project_id)
        queryset = project.contributors.all()
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']
        user_added_id = self.request.data['user']

        try:
            user = User.objects.get(id=user_added_id)
            project = Project.objects.get(pk=project_id)
            permission = 'CONTRIBUTOR'

        except User.DoesNotExist:
            raise APIException(f"User '{user}' does not exist.")
        except Project.DoesNotExist:
            raise APIException(f"Project '{project}' does not exist.")

        if Contributor.objects.filter(user=user, project=project).exists():
            raise APIException(f"User '{user}' is already a contributor of project '{project_id}'.")

        serializer.save(user=user, project=project, permission=permission)

    def destroy(self, request, pk=None, **kwargs):
        project_id = int(self.kwargs['project_pk'])
        user_id = int(pk)
        try:
            contribution = Contributor.objects.get(user=user_id, project=project_id)
        except Contributor.DoesNotExist:
            raise APIException("This contribution does not exist.")

        except contribution.project_id == project_id and contribution.permission == "CREATOR":
            raise APIException("Project's creator can't be removed from project")

        self.perform_destroy(contribution)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsObjectAuthor]

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)
        if 'pk' in self.kwargs:
            issue_id = self.kwargs['pk']
            return Issue.objects.filter(pk=issue_id, project=project)
        else:
            return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        user = self.request.user
        project_id = self.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)

        title = self.request.data['title']
        description = self.request.data['description']
        tag = self.request.data['tag']
        priority = self.request.data['priority']
        status = self.request.data['status']
        assignee_user = self.request.data['assignee_user']

        if assignee_user != "":
            contributors = [contributor.user for contributor in Contributor.objects.filter(project_id=project_id)]
            if serializer.validated_data['assignee_user'] not in contributors:
                raise ValidationError({"Assignee user must be a contributor of this project."})
            else:
                assignee_user = User.objects.get(id=assignee_user)
        else:
            assignee_user = User.objects.get(id=user.id)

        serializer.save(author_user=user,
                        project=project,
                        title=title,
                        description=description,
                        tag=tag,
                        priority=priority,
                        status=status,
                        assignee_user=assignee_user)

    perform_update = perform_create


class CommentViewset(ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = (IsAuthenticated, IsProjectContributor, IsObjectAuthor)

    def get_queryset(self):
        issue_id = self.kwargs['issue_pk']

        issue = get_object_or_404(Issue, pk=issue_id)
        if 'pk' in self.kwargs:
            comment_id = self.kwargs['pk']
            return Comment.objects.filter(pk=comment_id)
        else:
            return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        user = self.request.user
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])

        description = self.request.data['description']

        serializer.save(author_user=user, issue=issue, description=description)

    perform_update = perform_create
