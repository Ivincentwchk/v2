from rest_framework import serializers
from accounts.models import User, UserProfile, UserActivity, Subject, Course, UserCourse, Question, Option


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['score', 'rank', 'login_streak_days', 'last_login_date']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['userID', 'user_name', 'email', 'License', 'profile', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            License=validated_data.get('License')
        )
        return user


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['activity_type', 'timestamp', 'details']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['SubjectID', 'SubjectName', 'SubjectDescription']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['CourseID', 'SubjectID', 'CourseTitle', 'CourseDescription', 'CourseDifficulty']


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ['CourseID', 'UserID', 'CourseScore', 'CourseFlag']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['QuestionID', 'CourseID', 'QuestionDescription']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        # Expose everything including CorrectOption; we will control what is returned via views
        fields = ['OptionID', 'QuestionID', 'OptionText', 'CorrectOption']


class QuestionDetailSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['QuestionID', 'CourseID', 'QuestionDescription', 'options']

    def get_options(self, obj):
        # Return options without the CorrectOption field as required
        return [
            {
                'OptionID': option.OptionID,
                'OptionText': option.OptionText,
            }
            for option in obj.options.all()
        ]
