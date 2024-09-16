from django.db import models
from books.models import Copies
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class FlagTransaction(models.TextChoices):
    returned = 'Returned'
    active = 'Active'
    
class Histories(models.Model):
    book_copies = models.ForeignKey(Copies, verbose_name="BookCopies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FlagTransaction.choices, default=FlagTransaction.active)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    action_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_date is None:
            self.start_date = datetime.now()

        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=30)
            
        super().save(*args, **kwargs)
