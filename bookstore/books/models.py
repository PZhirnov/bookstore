# books/models.py
from django.contrib import admin
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.urls import reverse


AGE_GROUP = (
    (0, " < 13 "),
    (1, " > 13 "),
    (2, " > 19 "),
)

BOOK_FORMAT = (
    (0, 'PDF'),
    (1, 'Hard Cover'),
    (2, 'Epub'),
    (3, 'HTML'),
)


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(choices=AGE_GROUP, default=2)  # >19
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField()

    def __str__(self):
        return self.name

    @property
    def admin_name(self):
        return f'{self.name} ({self.website})'


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

    # url for book detail page
    def get_absolute_url(self):
        return reverse("books:bookdetail", kwargs={'pk': self.pk})

        # return reverse("book:bookdetail", args=[str(self.pk)])
        # return reverse("book:bookdetail", args=[str(self.id)])

    # url for booklist page
    def get_book_list_url(self):
        return reverse("books:booklist")


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


class Format(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_format = models.IntegerField(choices=BOOK_FORMAT, default=0)  # PDF
    price = models.DecimalField(decimal_places=2, max_digits=10)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    available = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.book} ({BOOK_FORMAT[self.book_format][1]})"

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.sale_price


# pre_save does not have "created" argument as post_save
def pre_save_add_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title)
        exists = Book.objects.filter(slug=new_slug).exists()
        if exists:
            new_slug = f'{new_slug}-{instance.id}'
        instance.slug = new_slug


pre_save.connect(pre_save_add_slug, sender=Book)


def post_save_format_for_book(sender, instance, created, *args, **kwargs):
    formats = instance.format_set_all()
    if formats.count() == 0:
        new_format = Format()
        new_format.book = instance
        new_format.book_format = 0
        new_format.price = 0.00
        new_format.save()


post_save.connect(post_save_format_for_book, sender=Book)
