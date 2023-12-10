from tabnanny import verbose
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 拡張ユーザモデル

    class Meta:
        verbose_name_plural = 'CustomUser'