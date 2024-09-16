from django.db import models

class Book(models.Model):
    isbn = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=254, null=False)
    author = models.CharField(max_length=254, null=False)
    publisher = models.CharField(max_length=254, null=False)
    edition = models.CharField(max_length=254)
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.isbn
    

class CopyStatus(models.TextChoices):
    AVAILABLE = 'Available'
    NOT_AVAILABLE = 'Not Available'


class Copies(models.Model):
    book = models.ForeignKey(Book, verbose_name="Book", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=CopyStatus.choices, default=CopyStatus.AVAILABLE)

    class Meta:
        verbose_name = "Copies"
        verbose_name_plural = "Copies"

    def __str__(self):
        return str(self.id) 
    
