from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .semester import Semester
from .course import Course

class StudentEnrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
        help_text="Final grade for the course (0.0 to 5.0)."
    )

    class Meta:
        unique_together = ("student", "semester", "course")
