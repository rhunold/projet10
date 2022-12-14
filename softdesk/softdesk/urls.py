from django.contrib import admin
from django.urls import path, include

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import ProjectViewset, ContributorsViewset, IssueViewset, CommentViewset
from api.views import SignUpView, ContributorsViewset

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_nested import routers
# from rest_framework import routers



router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')
# router.register('users', ContributorsViewset, basename='users')
# router.register('issues', IssueViewset, basename='issues')
# router.register('comments', CommentViewset, basename='comments')


# users_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
# users_router.register('users', ContributorsViewset, basename='users')

# issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
# issues_router.register('issues', IssueViewset, basename='issues')

# comments_router = routers.NestedSimpleRouter(issues_router, 'issues', lookup='issue')
# comments_router.register('comments', CommentViewset, basename='comments')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/', include('rest_framework.urls'))    
    
    # path('', include(router.urls)),

    path('signup/', SignUpView.as_view({'post': 'create'}), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('', include(router.urls)),
    # path('', include(users_router.urls)),
    # path('', include(issues_router.urls)),
    # path('', include(comments_router.urls)),
    
    
    # path('api-auth/', include('rest_framework.urls')),    
]

# urlpatterns += router.urls