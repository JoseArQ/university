from django.db import models
from django.conf import settings

from .semester import Semester

class StudentLoadSemester(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    max_credits = models.PositiveIntegerField()

    class Meta:
        unique_together = ("student", "semester")

    def __str__(self):
        return f"{self.student} - {self.semester}: {self.max_credits} credits"