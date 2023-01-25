from django.contrib import admin
from django.urls import path, include

from api.views import SignUpView, ContributorsViewset, ProjectViewset, ContributorsViewset, IssueViewset, CommentViewset

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_nested import routers


project_router = routers.SimpleRouter()
project_router.register('projects', ProjectViewset, basename='projects')

users_router = routers.NestedSimpleRouter(project_router, 'projects', lookup='project')
users_router.register('users', ContributorsViewset, basename='users')

issues_router = routers.NestedSimpleRouter(project_router, 'projects', lookup='project')
issues_router.register('issues', IssueViewset, basename='issues')

comments_router = routers.NestedSimpleRouter(issues_router, 'issues', lookup='issue')
comments_router.register('comments', CommentViewset, basename='comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view({'post': 'create'}), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(project_router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]

# urlpatterns += project_router