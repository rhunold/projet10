from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


TYPES = (
    ("BACKEND", "Back-end"),
    ("FRONTEND", "Front-end"),
    ("IOS", "iOS"),
    ("ANDROID", "Andorid"),
)

PRIORITIES = (
    ('LOW', 'Basse'),
    ('MEDIUM', 'Moyenne'),
    ('HIGH', 'Haute'),
)

TAGS = (
    ('BUG', 'Bug'),
    ('IMPROVE', 'Amélioration'),
    ('TASK', 'Tâche'),
)

STATUS = (
    ('TODO', 'A faire'),
    ('DOING', 'En cours'),
    ('DONE', 'Terminé'),
)

PERMISSIONS = (
    ('CREATOR', 'Créateur'),
    ('CONTRIBUTOR', 'Contributeur'),
)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, blank=True)
    type = models.CharField(max_length=20, choices=TYPES, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='projects', blank=True, null=False)

    def __str__(self):
        return f"{self.title} /  id {self.id} / by {self.author_user}"


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors', blank=False)
    permission = models.CharField(max_length=20, choices=PERMISSIONS, blank=True)
    role = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = (
            "user",
            "project",
        )

    def __str__(self):
        return f"{self.user} is a {self.permission} on project {self.project.id} with role {self.role}"


class Issue(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=1024, blank=False)
    tag = models.CharField(max_length=20, choices=TAGS, blank=False)
    priority = models.CharField(max_length=20, choices=PRIORITIES, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=20, choices=STATUS, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='author_user_issues')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='assignee_user_issues', null=True, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} on project {self.project.id} assigned to {self.assignee_user}"


class Comment(models.Model):
    description = models.CharField(max_length=1024, null=False, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.author_user} comment on issue {self.issue.id} : {self.description}"
