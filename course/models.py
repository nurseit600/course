from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from rest_framework.exceptions import ValidationError

ROLES_CHOICES = (
        ('teacher', 'teacher'),
        ('student', 'student'),
    )

STATUS_CHOICES = (
        ('легкий', 'легкий'),
        ('средний', 'средный'),
        ('сложный', 'сложный'),
    )


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(60)],
                                           null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Network(models.Model):
    network_name = models.CharField(max_length=32)
    network_link = models.URLField()
    title = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}, {self.network_name}'


class Teacher(UserProfile):
    bio = models.TextField()
    DAYS_CHOICES = (
        ('ПН', 'ПН'),
        ('ВТ', 'ВТ'),
        ('СР', 'СР'),
        ('ЧТ', 'ЧТ'),
        ('ПТ', 'ПТ'),
        ('СБ', 'СБ'),
    )
    work_days = MultiSelectField(max_length=16, choices=DAYS_CHOICES, max_choices=6)
    subjects = models.TextField()
    experience = models.PositiveSmallIntegerField(validators=[MaxValueValidator(40)])
    role = models.CharField(max_length=32, choices=ROLES_CHOICES, default='teacher')

    def __str__(self):
        return f'{self.first_name}, {self.role}'

    class Meta:
        verbose_name_plural = "teachers"


class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, choices=ROLES_CHOICES, default='student')

    def __str__(self):
        return f'{self.user}, {self.role}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Course(models.Model):
    course_name = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ManyToManyField(Category, related_name='category_course')
    author = models.ManyToManyField(Teacher)
    level = models.CharField(max_length=32, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    TYPE_CHOICES = (
        ('бесплатный', 'бесплатный'),
        ('платный', 'платный')
    )
    type_course = models.CharField(max_length=32, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_certificate = models.BooleanField(default=True,)
    course_image = models.ImageField(upload_to='course_image', null=True, blank=True)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    admin_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.course_name

    def get_average_rating(self):
        all_reviews = self.course_review.all()
        if all_reviews.exists():
            count_people = 0
            total_stars = 0
            for i in all_reviews:
                if i.stars is not None:
                    total_stars += i.stars
                    count_people += 1
            if count_people == 0:
                return 0
            return round(total_stars / count_people, 1)
        return 0

    def get_count_people(selfs):
        return selfs.course_review.count()

    def get_change_price(self):
        return self.price - self.admin_price


class Lesson(models.Model):
    title = models.CharField(max_length=64)
    video_url = models.URLField(null=True, blank=True)
    video = models.FileField(upload_to='course_videos', null=True, blank=True)
    content = models.FileField(upload_to='course_documents', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson_courses')

    def __str__(self):
        return f'{self.course}, {self.title}'


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=32)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment_courses')

    def __str__(self):
        return self.title


class Exam(models.Model):
    title = models.CharField(max_length=32)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_courses')
    end_time = models.DurationField()

    def __str__(self):
        return f'{self.title}, {self.course}'


class Questions(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                         MaxValueValidator(100)])

    def __str__(self):
        return f'{self.exam}, {self.title}'


class Option(models.Model):
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE)
    variant = models.CharField(max_length=64)
    option_check = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.variant}, {self.check}'


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_courses')
    issued_at = models.DateField(auto_now_add=True)
    certificate_url = models.FileField(upload_to='certificates')

    def __str__(self):
        return f'{self.student}, {self.course}'


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)],
                                        null=True, blank=True)

    def __str__(self):
        return f'{self.user}, {self.course}'

    def clean(self):
        super().clean()
        if not self.text and not self.stars:
            raise ValidationError('Choose minimum one of (text, stars)!')


class TeacherRating(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return f'{self.teacher}, {self.stars}'


class History(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course


class Cart(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Favorite(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)






