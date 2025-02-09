from .models import Course, Teacher, Category, Questions, Exam, Network, Lesson, Assignment, Option
from modeltranslation.translator import TranslationOptions, register


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('course_name', 'description')


@register(Teacher)
class TeacherTranslationOptions(TranslationOptions):
    fields = ('bio', 'subjects')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('option_check',)


@register(Questions)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Exam)
class ExamTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Network)
class NetworkTranslationOptions(TranslationOptions):
    fields = ('title', 'user', 'network_name')


@register(Lesson)
class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(Assignment)
class AssignmentTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

