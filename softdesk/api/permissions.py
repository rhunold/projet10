from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from .models import Contributor, Project
from rest_framework.exceptions import APIException


class IsProjectContributor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        user_id = user.id

        contributions_of_user = [contrib.project_id for contrib in user.contributors.filter(user=user_id)]

        if 'project_pk' in view.kwargs:
            project_id = int(view.kwargs['project_pk'])
        elif 'pk' in view.kwargs:
            project_id = int(view.kwargs['pk'])
        else:
            project_id = None

        if contributions_of_user is None:
            return print("This user is not associated to any project.")

        if project_id is None:
            return True

        if project_id in contributions_of_user:
            return True


class IsObjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if (obj.author_user == request.user or view.action in ['retrieve', 'list']) or request.user.is_superuser:
            return True


class IsProjectCreator(BasePermission):
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)

        try:
            user_contrib = Contributor.objects.get(project=project, user=request.user)

        except Contributor.DoesNotExist:
            raise APIException("You can't access users of a project you not belong too.")

        if user_contrib.permission == 'CREATOR':
            return True

        if user_contrib.permission == 'CONTRIBUTOR' and view.action in ['list', 'retrieve']:
            return True
