from django.contrib.auth.models import User
from django.contrib import admin
from apps.account.models import Profile
from django.template.loader import render_to_string


@admin.display(description="Previa imagen de perfil actual")
def cover_preview_display(obj):
    return render_to_string(
        "cover.html", dict(url=obj.avatar.url, empty_message="Sin avatar")
    )


# Foreign keys
class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = "user"
    exclude = ("pk",)
    readonly_fields = [cover_preview_display]


# Object
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    inlines = [ProfileInline]
    search_fields = ["email"]
    list_filter = ["is_active"]
    exclude = (
        "password",
        "last_session",
        "user_permissions",
        "representedgroup",
        "last_login",
        "groups",
        "logentry",
    )
