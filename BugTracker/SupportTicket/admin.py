from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Project, Ticket, User


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    search_field = ('email', 'first_name', 'last_name', 'role')
    readonly_fields = ()

    filter_horizontal = ()
    list_filter = ()
    ordering = ()
    fieldsets = ()


admin.site.register(User, AccountAdmin)

admin.site.register(Project)
admin.site.register(Ticket)
