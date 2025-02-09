from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet),
router.register(r'networks', NetworkViewSet),
router.register(r'teachers', TeacherViewSet),
router.register(r'questions', QuestionsViewSet),
router.register(r'options', OptionViewSet),
router.register(r'student', StudentViewSet),
router.register(r'teacher_ratings', TeacherRatingViewSet),
router.register(r'history', HistoryViewSet),
router.register(r'carts', CartViewSet),
router.register(r'cart_items', CartItemViewSet),
router.register(r'favorites', FavoriteViewSet),
router.register(r'favorite_item', FavoriteItemViewSet, basename='favorite_items'),

urlpatterns = [
    path('', include(router.urls)),
    path('courses/', CourseListAPIView.as_view(), name='courses_list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='courses_list'),

    path('categories/', CategoryListAPIView.as_view(), name='categories_List'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),

    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('assignment/', AssignmentListAPIView.as_view(), name='assignment_list'),
    path('certificate/', CertificateListAPIView.as_view(), name='certificate_list'),
    path('course_review/', CourseListReviewAPIView.as_view(), name='course_review_list'),
    path('exam/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/<int:pk>/', ExamDetailAPIView.as_view(), name='exam_detail'),

]


