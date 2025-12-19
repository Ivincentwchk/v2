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
    profile_pic = models.BinaryField(null=True, blank=True)
    profile_pic_mime = models.CharField(max_length=100, null=True, blank=True)
    bookmarked_subject = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL, related_name='bookmarked_users')
    bookmarked_subject_updated_at = models.DateTimeField(null=True, blank=True)

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


class Achievement(models.Model):
    key = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=32)
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=32)
    target = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    progress = models.IntegerField(default=0)
    unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.user_name} - {self.achievement.key}"


class Subject(models.Model):
    SubjectID = models.AutoField(primary_key=True)
    SubjectName = models.CharField(max_length=255)
    SubjectDescription = models.TextField()
    icon_svg_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.SubjectName


class SubjectBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_bookmarks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.user_name} bookmarked {self.subject.SubjectName}"


class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    SubjectID = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    CourseTitle = models.CharField(max_length=255)
    CourseDescription = models.TextField()
    CourseDifficulty = models.IntegerField()
    Content = models.TextField(blank=True, default="")

    def __str__(self):
        return self.CourseTitle


class UserCourse(models.Model):
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_courses')
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_courses')
    CourseScore = models.CharField(max_length=255)
    CourseFlag = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.UserID.user_name} - {self.CourseID.CourseTitle}"


class Question(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    QuestionDescription = models.TextField()

    def __str__(self):
        return f"Question {self.QuestionID} for {self.CourseID.CourseTitle}"


class Option(models.Model):
    OptionID = models.AutoField(primary_key=True)
    QuestionID = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    OptionText = models.TextField()
    CorrectOption = models.BooleanField()

    def __str__(self):
        return f"Option {self.OptionID} for Question {self.QuestionID_id}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset token for {self.user.user_name} (used={self.used})"

