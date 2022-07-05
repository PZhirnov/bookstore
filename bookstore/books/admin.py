from django.contrib import admin
from .models import Author, Book, BookImage, Publisher, Format
from django.utils import timezone
from .forms import AuthorForm

# Register your models here.


def draft_status(modeladmin, request, queryset):
    queryset.update(
        draft=False,
        publication_date=timezone.now()
    )


draft_status.short_description = 'Mark book as published now'


# Modify admin page
class AuthorAdmin(admin.ModelAdmin):
    # Укажем поля, которые будут отображать в модели
    list_display = ['first_name', 'last_name', 'email']
    # Добавим сортировку данных в модели
    ordering = ['last_name', 'email']
    list_filter = ['last_name']
    form = AuthorForm
    save_as = False  # enable save as option
    # save_on_top = True  # show the save-buttons on top and bottom
    radio_fields = {'age': admin.HORIZONTAL}  # admin.VERTICAL

# Первый способ регистрации модели в админке
admin.site.register(Author, AuthorAdmin) # добавить наследование


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['admin_name']


# Action fields
def draft_status(modeladmin, request, queryset):
    queryset.update(
        draft=False,
        publication_date=timezone.now()
    )


draft_status.short_description = 'Mark book as published now' # at admin page


# Второй способ регистрации модели в админке - с помощью декоратора
class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 5


class BookInline(admin.TabularInline):
    model = Book
    extra = 1  # show only one item


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'publisher', 'draft', 'updated']
    list_editable = ['publisher', 'draft']
    search_fields = ['title', 'publisher__country', 'authors__last_name']
    actions = [draft_status]
    date_hierarchy = 'publication_date'  # Date hierarchy
    filter_horizontal = ['authors']
    prepopulated_fields = {'slug': ('title',)}
    # fields = [
    #     ('title', 'slug', 'draft'),
    #     ('authors', 'publisher'),
    #     'content',
    #     'publication_date',
    # ]

    # both 'fields' and 'fieldsets' can not be specified together
    fieldsets = (
        (None, {  # label 1: None
            'fields': (  # dictionary
                ('title', 'slug'),

            )
        }),
        ('More details', {  # under label 2 : More details
            'classes': ('collapse',),  # css-class : minimized
            'fields': (
                ('authors', 'publisher'),
                'content',
                ('draft', 'publication_date'),
            )
        })
    )
    inlines = [BookImageInline]


admin.site.register(BookImage)
# admin.site.register(Publisher)
# admin.site.register(Book)


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    save_as = True  # enable save as option
    save_on_top = True  # show th save-buttons on top and bottom
    radio_fields = {'book_format': admin.HORIZONTAL}  # admin.VERTICAL
