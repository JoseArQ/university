from django.db import models
from django.conf import settings

from .semester import Semester

class TeacherLoadSemester(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    max_credits = models.PositiveIntegerField()

    class Meta:
        unique_together = ("teacher", "semester")

    def __str__(self):
        return f"{self.teacher} - {self.semester}: {self.max_credits} credits"
