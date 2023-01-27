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
    type = models.CharField(max_length=20, blank=True, choices=TYPES)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributors')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors', blank=False)
    permission = models.CharField(max_length=20,choices=PERMISSIONS, blank=True)
    role = models.CharField(max_length=128, blank=True)

    class Meta:
        unique_together = (
            "user",
            "project",
        )
        # ordering = ["user_id"]

    def __str__(self):
        return self.permission



class Issue(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=1024, blank=False)
    tag = models.CharField(max_length=20, choices=TAGS, blank=False)
    priority = models.CharField(max_length=20, choices=PRIORITIES, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    status = models.CharField(max_length=20, choices=STATUS, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_user_issues')
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignee_user_issues', null=True, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.CharField(max_length=1024, null=False, blank=False)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description