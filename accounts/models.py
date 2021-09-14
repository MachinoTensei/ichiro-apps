from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone



class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    email = models.EmailField('メールアドレス', unique=True)
    first_name = models.CharField('姓', max_length=150)
    last_name = models.CharField('名', max_length=150)
    address = models.CharField('住所', max_length=150, blank=True)
    tel = models.CharField('電話番号', max_length=150, blank=True)
    created = models.DateTimeField('入会日', default=timezone.now)
    """
    email = models.EmailField('メールアドレス', unique=True)
    site_name = models.CharField('サイト名', max_length=150)
    company = models.CharField('会社名', max_length=150)
    address = models.CharField('所在地', max_length=150, blank=True)
    tel = models.CharField('電話番号', max_length=150, blank=True)
    fax = models.CharField('FAX', max_length=150, blank=True)
    created = models.DateTimeField('登録日', default=timezone.now)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)