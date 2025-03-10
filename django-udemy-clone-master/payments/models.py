from django.db import models

# Create your models here.
# payments/models.py

from django.db import models
from django.conf import settings
from courses.models import Course

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Add other relevant fields as needed

    def __str__(self):
        return f"{self.user} - {self.course} - {self.amount}"
