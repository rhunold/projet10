from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import APIException
from .models import Contributor



def get_project_id(kwargs):
    project_id = kwargs['project_pk'] if 'project_pk' in kwargs else kwargs['pk'] if 'pk' in kwargs else None
    if project_id is None:
        return project_id
    else:
        try:
            return int(project_id)
        except ValueError:
            raise APIException({"details": 'Project ids must be integers.'})


class IsProjectContributor(BasePermission):
    # message = "You don't have access to this project"

    def has_permission(self, request, view):
        # List the projects on which the user is a contributor or creator
        user = request.user

        if user.is_superuser:
            return True
        
        project_id = get_project_id(view.kwargs)        
        user_id = user.id
                
        contributions_of_user = [contrib.project_id for contrib in user.contributors.filter(user=user_id)]
        
        if contributions_of_user is None:
            return print("This user is not associated to any project.")
            
        if project_id is None or project_id in contributions_of_user:
            return True


    def has_object_permission(self, request, view, obj):
        # List of method allowed for the user on a project
        user = request.user
        user_id = user.id        
        project_id = get_project_id(view.kwargs)
        contributions_of_user = [contrib.project_id for contrib in user.contributors.filter(user=user_id)] # , permission="CONTRIBUTOR"

        if project_id in contributions_of_user: # and view.action in ['list', 'retrieve']
            return True


class IsObjectCreator(BasePermission):    
    def has_object_permission(self, request, view, obj):
        if obj.author_user == request.user or view.action in ['list', 'retrieve']:
            return True


class IsProjectCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        project_id = get_project_id(view.kwargs)
        user_contrib = Contributor.objects.get(project_id=project_id, user=request.user)
        if user_contrib.permission == 'CREATOR':
            return True
