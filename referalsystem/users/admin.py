from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number",)
    fields = (
        "username", "first_name",
        "last_name", "phone_number",
        "invite_code", "inviter",
        "confirmation_code",
        "is_active",
        "is_staff",
    )
    readonly_fields = ("invite_code",)

admin.site.register(User, UserAdmin)
