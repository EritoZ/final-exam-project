import autoslug
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models as db_models
from django.contrib.auth import models as auth_models
from django.utils import timezone


# Create your models here.

class UserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    genders = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Do not show'),
    )

    username_validator = UnicodeUsernameValidator()

    username = db_models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = db_models.CharField(
        "first name",
        max_length=30,
        validators=[validators.MinLengthValidator(2)],
        blank=True
    )

    last_name = db_models.CharField(
        "last name",
        max_length=30,
        validators=[validators.MinLengthValidator(2)],
        blank=True
    )

    email = db_models.EmailField("email address", blank=True, unique=True)

    profile_image = db_models.ImageField("profile image", upload_to='profile images', blank=True, null=True)

    gender = db_models.CharField(
        choices=genders,
        default='3'
    )

    slug = autoslug.AutoSlugField(populate_from='username')

    is_staff = db_models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = db_models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = db_models.DateTimeField(("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
