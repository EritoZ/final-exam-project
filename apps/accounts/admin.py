from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # List the fields you want to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'gender',
                    'last_login', 'date_joined')

    # Add filters by gender, staff status, and active status
    list_filter = ('gender', 'is_staff', 'is_active')

    # Enable search by username, email, first name, and last name
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Define the order in which the fields are listed in the admin view
    ordering = ('username', 'last_login')

    # Custom actions
    actions = ['make_active', 'make_inactive', 'make_staff', 'unmake_staff']

    sortable_by = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    make_active.short_description = "Mark selected users as active"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_inactive.short_description = "Mark selected users as inactive"

    def make_staff(self, request, queryset):
        queryset.update(is_staff=True)

    make_staff.short_description = "Mark selected users as staff"

    def unmake_staff(self, request, queryset):
        queryset.update(is_staff=False)

    unmake_staff.short_description = "Unmark selected users as staff"

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)

            if obj.password != orig_obj.password:  # password changed
                obj.set_password(obj.password)

        else:
            obj.set_password(obj.password)

        obj.save()
