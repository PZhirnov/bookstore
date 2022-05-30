from django.contrib import admin
from .models import Author, Book, BookImage, Publisher

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookImage)
admin.site.register(Publisher)
