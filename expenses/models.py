from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} — {self.amount}"