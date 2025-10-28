from django.db import models
from django.conf import settings

from .semester import Semester
from .course import Course


class CourseOffering(models.Model):
    """
    Represents a specific instance of a course offered during a given semester by a teacher.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="offerings",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "TEACHER"},
        related_name="course_offerings",
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="course_offerings",
    )

    class Meta:
        unique_together = ("course", "semester", "teacher")
        verbose_name = "Course Offering"
        verbose_name_plural = "Course Offerings"

    def __str__(self):
        return f"{self.course.code} ({self.semester}) - {self.teacher.username}"
