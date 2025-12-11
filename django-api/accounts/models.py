import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not user_name:
            raise ValueError('The User name field must be set')
        email = self.normalize_email(email)
        user = self.model(user_name=user_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        # Create profile
        UserProfile.objects.create(user=user)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    License = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=99999)
    login_streak_days = models.IntegerField(default=0)
    last_login_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_name}'s profile"


class UserActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('REGISTRATION', 'Registration'),
        ('SCORE_UPDATE', 'Score Update'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.activity_type} at {self.timestamp}"


class Subject(models.Model):
    SubjectID = models.AutoField(primary_key=True)
    SubjectName = models.CharField(max_length=255)
    SubjectDescription = models.TextField()

    def __str__(self):
        return self.SubjectName


class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    SubjectID = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    CourseTitle = models.CharField(max_length=255)
    CourseDescription = models.TextField()
    CourseDifficulty = models.IntegerField()

    def __str__(self):
        return self.CourseTitle


class UserCourse(models.Model):
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_courses')
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_courses')
    CourseScore = models.CharField(max_length=255)
    CourseFlag = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.UserID.user_name} - {self.CourseID.CourseTitle}"
