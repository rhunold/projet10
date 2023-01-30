from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from .models import Contributor, Project


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
            return print(f"This user is not associated to any project.")

        if project_id is None:
            return True
        
        if project_id in contributions_of_user:
            return True


class IsObjectAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author_user == request.user or view.action in ['list', 'retrieve']:
            return True


class IsProjectCreator(BasePermission):
    def has_object_permission(self, request, view, obj):

        project_id = view.kwargs.get('project_pk')
        project = get_object_or_404(Project, id=project_id)
        
        user_contrib = Contributor.objects.get(project=project, user=request.user)
                
        if user_contrib.permission == 'CREATOR' and view.action in ['create', 'destroy']:
            return True