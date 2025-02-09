from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class CourseListSerializer(serializers.ModelSerializer):
    author = UserProfileCourseSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    get_change_price = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_image', 'level', 'type_course',
                  'author', 'price', 'old_price', 'average_rating', 'count_people', 'get_change_price']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_change_price(self, obj):
        return obj.get_change_pric()


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_course = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_course']


class LessonListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'video']


class AssignmentListSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(format='%d-%m-%Y  %H:%M')

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']


class CertificateListSerializer(serializers.ModelSerializer):
    student = UserProfileCourseSerializer()
    issued_at = serializers.DateField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Certificate
        fields = ['student', 'certificate_url', 'issued_at']


class CourseListReviewSerializer(serializers.ModelSerializer):
    user = UserProfileCourseSerializer()

    class Meta:
        model = CourseReview
        fields = ['user', 'text', 'stars']


class ExamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'end_time', 'title', ]


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategoryCourseSerializer(many=True)
    author = UserProfileCourseSerializer(many=True)
    created_at = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    updated_at = serializers.DateTimeField(format='%d-%m-%Y  %H:%M')
    lesson_courses = LessonListSerializer(many=True)
    assignment_courses = AssignmentListSerializer(many=True)
    course_review = CourseListReviewSerializer(many=True)
    exam_courses = ExamListSerializer(many=True)
    certificate_courses = CertificateListSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['course_name', 'category', 'description', 'course_image', 'level', 'type_course',
                  'author', 'price', 'created_at', 'updated_at', 'course_certificate',
                  'average_rating', 'count_people', 'lesson_courses', 'assignment_courses',
                  'course_review', 'exam_courses', 'certificate_courses']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class ExamDetailSerializer(serializers.ModelSerializer):
    exam_courses = CourseListSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['end_time', 'title', ]


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class TeacherRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRating
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteItem
        fields = '__all__'

