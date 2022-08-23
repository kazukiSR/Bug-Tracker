# Generated by Django 4.1 on 2022-08-11 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Submitter'), (2, 'Developer'), (3, 'Project Manager'), (4, 'Admin')], null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'permissions': (('can_create_ticket', 'Can create tickets'), ('can_resolve_ticket', 'Can change status of tickets'), ('can_assign_ticket', 'Can assign tickets to developers'), ('can_create_project', 'Can create projects'), ('can_assign_dev_project', 'Can assign developers to projects'), ('can_assign_manager_project', 'Can assign project managers to projects'), ('can_assign_roles', 'Can assign users to roles')),
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=256)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Open'), (2, 'In Progress'), (3, 'Resolved'), (4, 'Additional Info Required')], default=(1, 'Open'))),
                ('priority', models.PositiveSmallIntegerField(choices=[(1, 'None'), (2, 'Low'), (3, 'Medium'), (4, 'High')], default=(1, 'None'))),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Bugs/Errors'), (2, 'Feature Requests'), (3, 'Document Requests'), (4, 'Other Comments')], default=(1, 'Bugs/Errors'))),
                ('assigned_developer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_developer', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SupportTicket.project')),
                ('submitter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket_submitter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='assigned_developers',
            field=models.ManyToManyField(related_name='project_developers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='project_managers',
            field=models.ManyToManyField(related_name='project_managers', to=settings.AUTH_USER_MODEL),
        ),
    ]