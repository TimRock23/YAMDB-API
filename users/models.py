from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        username = email.split('@')[0]
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user', _('Обычный пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(max_length=250, blank=True)
    role = models.CharField(
        max_length=9, choices=UserRole.choices, default=UserRole.USER
    )
    confirmation_code = models.CharField(max_length=15)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    STAFF = [UserRole.MODERATOR, UserRole.ADMIN]

    objects = UserManager()

    @property
    def is_admin_or_moder(self):
        return self.role in self.STAFF or self.is_superuser

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
