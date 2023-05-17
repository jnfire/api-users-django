from django.db import models
from django.contrib.auth.models import User
from core.settings import DOMAIN_URL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar_images", blank=True)

    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def avatar_url(self):
        return f"{DOMAIN_URL}{self.avatar.url}" if self.avatar else ""

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.enail
