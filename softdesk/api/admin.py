from django.contrib import admin
from .models import User, Project

class UserAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)