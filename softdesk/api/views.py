
# from rest_framework.views import APIView
from rest_framework.response import Response


from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import  UserSerializer


class SignUpView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    



class ProjectViewset(ModelViewSet):
    pass


class IssueViewset(ModelViewSet):
    pass


class CommentViewset(ModelViewSet):
    pass


class ContributorsViewset(ModelViewSet):
    pass







