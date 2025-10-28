from django.db import models

class Semester(models.Model):
    year = models.PositiveIntegerField()
    term = models.PositiveSmallIntegerField(choices=[(1, "First"), (2, "Second")])

    class Meta:
        unique_together = ("year", "term")

    def __str__(self):
        return f"{self.year}-{self.term}"
