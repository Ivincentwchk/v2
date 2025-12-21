from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Course, Subject, Question, Option, UserCourse, UserActivity
from accounts.serializers import (
    CourseSerializer,
    SubjectSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
)


@api_view(['GET'])
def list_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCourseListBySubjectID(request, subject_id):
    courses = Course.objects.filter(SubjectID_id=subject_id).only('CourseID', 'CourseTitle')
    serializer = CourseSerializer(courses, many=True)
    data = [{'CourseID': item['CourseID'], 'CourseTitle': item['CourseTitle']} for item in serializer.data]
    return Response(data)


@api_view(['GET'])
def getCourseByCourseID(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['GET'])
def getQuestionListByCourseID(request, course_id):
    questions = Question.objects.filter(CourseID_id=course_id).only('QuestionID')
    serializer = QuestionSerializer(questions, many=True)
    data = [item['QuestionID'] for item in serializer.data]
    return Response(data)


@api_view(['GET'])
def getQuestionByQuestionID(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({'detail': 'Question not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = QuestionDetailSerializer(question)
    return Response(serializer.data)


@api_view(['GET'])
def verifyAnsByOptionID(request, option_id):
    try:
        option = Option.objects.get(pk=option_id)
    except Option.DoesNotExist:
        return Response({'detail': 'Option not found.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'correct': bool(option.CorrectOption)})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submitCourseAnswers(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    answers = request.data.get('answers')
    if not isinstance(answers, list):
        return Response({'detail': 'answers must be a list.'}, status=status.HTTP_400_BAD_REQUEST)

    course_questions = list(Question.objects.filter(CourseID_id=course_id).only('QuestionID'))
    course_question_ids = {q.QuestionID for q in course_questions}

    if not course_question_ids:
        return Response({'detail': 'Course has no questions.'}, status=status.HTTP_400_BAD_REQUEST)

    normalized_answers = {}
    invalid_items = []

    for idx, item in enumerate(answers):
        if not isinstance(item, dict):
            invalid_items.append({'index': idx, 'detail': 'Each answer must be an object.'})
            continue

        question_id = item.get('question_id')
        option_id = item.get('option_id')

        try:
            question_id_int = int(question_id)
            option_id_int = int(option_id)
        except (TypeError, ValueError):
            invalid_items.append({'index': idx, 'detail': 'question_id and option_id must be integers.'})
            continue

        normalized_answers[question_id_int] = option_id_int

    if invalid_items:
        return Response({'detail': 'Invalid answers payload.', 'errors': invalid_items}, status=status.HTTP_400_BAD_REQUEST)

    submitted_question_ids = set(normalized_answers.keys())
    extra_question_ids = sorted(list(submitted_question_ids - course_question_ids))
    if extra_question_ids:
        return Response(
            {'detail': 'Some submitted questions are not part of this course.', 'extra_question_ids': extra_question_ids},
            status=status.HTTP_400_BAD_REQUEST,
        )

    missing_question_ids = sorted(list(course_question_ids - submitted_question_ids))
    if missing_question_ids:
        return Response(
            {'detail': 'You must answer all questions before submitting.', 'missing_question_ids': missing_question_ids},
            status=status.HTTP_400_BAD_REQUEST,
        )

    correct_count = 0
    per_question = []

    for question_id in sorted(course_question_ids):
        option_id = normalized_answers[question_id]

        try:
            option = Option.objects.get(pk=option_id)
        except Option.DoesNotExist:
            return Response(
                {'detail': 'Option not found.', 'question_id': question_id, 'option_id': option_id},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if option.QuestionID_id != question_id:
            return Response(
                {
                    'detail': 'Option does not belong to the submitted question.',
                    'question_id': question_id,
                    'option_id': option_id,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_correct = bool(option.CorrectOption)
        if is_correct:
            correct_count += 1

        per_question.append({'question_id': question_id, 'option_id': option_id, 'correct': is_correct})

    total_questions = len(course_question_ids)
    new_score_int = int(correct_count)

    user = request.user

    try:
        profile = user.profile
        profile.bookmarked_subject = course.SubjectID
        profile.bookmarked_subject_updated_at = timezone.now()
        profile.save(update_fields=['bookmarked_subject', 'bookmarked_subject_updated_at'])
    except Exception:
        pass

    user_course, created = UserCourse.objects.get_or_create(
        CourseID=course,
        UserID=user,
        defaults={
            'CourseScore': str(new_score_int),
            'CourseFlag': 'completed',
        },
    )

    improved = False
    if not created:
        try:
            existing_score_int = int(user_course.CourseScore)
        except (TypeError, ValueError):
            existing_score_int = 0

        if new_score_int > existing_score_int:
            user_course.CourseScore = str(new_score_int)
            improved = True

        user_course.CourseFlag = 'completed'
        user_course.save()

    UserActivity.objects.create(
        user=user,
        activity_type='SCORE_UPDATE',
        details=f"Course {course_id} submitted: {correct_count}/{total_questions} (improved={improved})",
    )

    return Response(
        {
            'course_id': course.CourseID,
            'total': total_questions,
            'correct': correct_count,
            'score': new_score_int,
            'best_score': int(user_course.CourseScore),
            'improved': improved,
            'completed': True,
            'per_question': per_question,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def markCourseCompletedByCourseID(request, course_id):
    score = request.data.get('score')
    if score is None:
        return Response({'detail': 'score is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_score_int = int(score)
    except (TypeError, ValueError):
        return Response({'detail': 'score must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        profile = user.profile
        profile.bookmarked_subject = course.SubjectID
        profile.bookmarked_subject_updated_at = timezone.now()
        profile.save(update_fields=['bookmarked_subject', 'bookmarked_subject_updated_at'])
    except Exception:
        pass

    user_course, created = UserCourse.objects.get_or_create(
        CourseID=course,
        UserID=user,
        defaults={
            'CourseScore': str(new_score_int),
            'CourseFlag': 'completed',
        },
    )

    if not created:
        try:
            existing_score_int = int(user_course.CourseScore)
        except (TypeError, ValueError):
            existing_score_int = 0

        if new_score_int > existing_score_int:
            user_course.CourseScore = str(new_score_int)

        user_course.CourseFlag = 'completed'
        user_course.save()

    return Response(
        {
            'CourseID': course.CourseID,
            'CourseFlag': user_course.CourseFlag,
            'CourseScore': user_course.CourseScore,
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCompletedCourse(request):
    user = request.user
    completed = UserCourse.objects.filter(UserID=user, CourseFlag='completed').values_list('CourseID_id', flat=True)
    return Response(list(completed))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCompletedCourseScores(request):
    user = request.user
    completed = UserCourse.objects.filter(UserID=user, CourseFlag='completed').only('CourseID_id', 'CourseScore')

    data = []
    for item in completed:
        try:
            score_int = int(item.CourseScore)
        except (TypeError, ValueError):
            score_int = 0
        data.append({'CourseID': item.CourseID_id, 'CourseScore': score_int})

    return Response(data)
