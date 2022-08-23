from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True, max_length=256)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    SUBMITTER = 1
    DEVELOPER = 2
    PROJECT_MANAGER = 3
    ADMIN = 4

    ROLE_CHOICES = (
        (SUBMITTER, 'Submitter'),
        (DEVELOPER, 'Developer'),
        (PROJECT_MANAGER, 'Project Manager'),
        (ADMIN, 'Admin')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        permissions = (
            ("can_create_ticket", "Can create tickets"),
            ("can_resolve_ticket", "Can change status of tickets"),
            ("can_assign_ticket", "Can assign tickets to developers"),
            ("can_create_project", "Can create projects"),
            ("can_assign_dev_project", "Can assign developers to projects"),
            ("can_assign_manager_project", "Can assign project managers to projects"),
            ("can_assign_roles", "Can assign users to roles")
        )

    def __str__(self):
        return self.first_name


class Ticket(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=256)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)

    assigned_developer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ticket_developer', blank=True, null=True)
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ticket_submitter', blank=True, null=True)

    date_created = models.DateTimeField(default=now, editable=False)
    date_modified = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        (1, 'Open'),
        (2, 'In Progress'),
        (3, 'Resolved'),
        (4, 'Additional Info Required')
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    PRIORITY_CHOICES = (
        (1, 'None'),
        (2, 'Low'),
        (3, 'Medium'),
        (4, 'High'),
    )
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES[0])
    TYPE_CHOICES = (
        (1, 'Bugs/Errors'),
        (2, 'Feature Requests'),
        (3, 'Document Requests'),
        (4, 'Other Comments')
    )
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0])

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=256)
    project_managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_managers', blank=True)
    assigned_developers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_developers', blank=True)

    def __str__(self):
        return self.title
