from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)  # Optional biography

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')  # Allow null if genre is unknown
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, blank=True) # ISBN (International Standard Book Number)
    summary = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)  # Available copies in stock
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    def is_available(self):
        return self.stock > 0

# Example of a ManyToMany relationship (if a book can have multiple genres)
# class Book(models.Model):
#     # ... other fields
#     genres = models.ManyToManyField(Genre, related_name="books", blank=True)
#     # ...
