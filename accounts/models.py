# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

#입력필드: id, password(상속), 닉네임, 사진, 한마디

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, nickname, password, **extra_fields):

        if not email:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, nickname=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, nickname, password, **extra_fields)

    def create_superuser(self, email, nickname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, nickname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    #id
    email = models.CharField(
        verbose_name=_('email'),
        max_length=30,
        unique=True,
    )

    #닉네임
    nickname = models.CharField(
        verbose_name=_('nickname'),
        max_length=30,
        unique=True,
        blank=False,
    )
    
    #사진
    photo = models.ImageField(
        verbose_name=_('profil photo'),
        upload_to="account/%Y/%m/%d",
        blank=True,
        null=True,
    )

    #가입날짜
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    
    last_login = models.DateTimeField(
        verbose_name=_('last login'),
        default=timezone.now
    )

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.nickname

    def get_full_name(self):        
        return self.nickname

    def get_short_name(self):
        return self.nickname
    
    def delete(self):
        self.photo.delete()
        super(User,self).delete()

    get_full_name.short_description = _('Full name')