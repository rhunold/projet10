from django.contrib import admin
from .models import User, Contributor, Project, Issue, Comment


class UserAdmin(admin.ModelAdmin):
    pass


class ContributorAdmin(admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
