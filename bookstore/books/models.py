# books/models.py

from django.db import models
from django.utils.text import slugify


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField()


class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    content = models.TextField()
    draft = models.BooleanField(default=True)
    publication_date = models.DateField(null=True, blank=True)
    # verbose_name can be defined in following two ways
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created on")
    updated = models.DateTimeField("Last updated", auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


# upload location : upload/book/title/slug.jpg
def upload_location(instance, filename):
    title = slugify(instance.book.title)  # Meher Baba -> Meher-Baba
    slug = instance.book.slug
    name, extension = filename.split(".")
    new_name = "%s.%s" % (slug, extension)
    return "book/%s/%s" % (title, new_name)


class BookImage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    def __str__(self):  # self.image is location
        return "%s (%s)" % (self.book.title, self.image)
