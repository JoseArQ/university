from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="dependent_courses",
        help_text="Courses that must be completed before taking this one."
    )

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def clean(self):
        """
        Prevent self-dependency in prerequisite relationships.
        """
        super().clean()

        if self.pk and self in self.prerequisites.all():
            raise ValidationError("A course cannot be a prerequisite of itself.")

    def __str__(self):
        return f"{self.code} - {self.name}"
