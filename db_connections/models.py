from django.db import models

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.title} ({self.instructor.name})"


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # e.g. 87.50 (%)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} in {self.course.title}"
