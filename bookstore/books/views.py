from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import Book, Author
from django.db.models import Q
from .forms import AuthorForm

# Main views

# display list of books using function based views


def book_list(request):
    template_name = "books/book_list.html"
    queryset = Book.objects.all()
    context = {
        "name": "Meher Kristina Patel",
        "object_list": queryset,
    }
    return render(request, template_name, context)


class BookList(ListView):
    # # default template Location: LowercaseAppName/LowercseAppName_list.html
    # template_name = "books/book_list.html"

    queryset = Book.objects.all()  # 'queryset' is reserved name like 'template_name'

    # to pass more context, inherit context with 'super' and
    #  then include the items in the context using "get_context_data"
    def get_context_data(self, *args, **kwargs):
        context = super(BookList, self).get_context_data(*args, **kwargs)
        context['name'] = "Harry"
        return context


# book details using class based view
class BookDetail(DetailView):
    model = Book  # use this or below
    # queryset = Book.objects.all()
    # template_name = 'books/test.html'

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data()
        print(context['object'].slug)
        return context


# ПРОЧИЕ ПРИМЕРЫ VIEWS
def http_example(request):
    return HttpResponse("<h3>This id HttpResponse </h3><p>Thank You!</p>")


def fexample(request):
    template_name = 'books/context_ex.html'  # user defined name 'template_name'
    context = {
        "name": "Market ",
        "fruits": ["apple", "orange", "banana"]
    }
    return render(request, template_name, context)


class CExample(TemplateView):
    template_name = 'books/context_ex.html'  # template_name is predefined

    def get_context_data(self, *args, **kwargs):
        context = {
            "name": "Harry",
            "fruits": ["pear", "cherry", "berry"]
        }
        return context


# read args using function-based view
def read_arg(request, val):
    print(request.method)  # если нужно получить наименование использовнаного метода
    print(request.headers)  # если нужно получить заголовки
    # если нужно получить переданные параметры в url
    # http://127.0.0.1:8000/books/freadargs/test/?testpar=RRRRRRRR  - testpar
    print(request.GET)  # если нужно получить словарь с параметрами или **kwargs
    template_name = 'books/read_url.html'
    context = {
        "value": val,
    }
    return render(request, template_name, context)


# read kwargs using function-based view
def read_kwarg(request, test):
    template_name = 'books/read_url.html'
    context = {
        "value": test
    }
    return render(request, template_name, context)


# read *args using class-based view
class ReadArg(TemplateView):
    template_name = 'books/read_url.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReadArg, self).get_context_data(*args, **kwargs)
        # test is defined in 'url'
        print('сработал')
        context['value'] = self.args[0]
        return context


# read kwargs using class-based view
class ReadKwarg(TemplateView):
    template_name = 'books/read_url.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReadKwarg, self).get_context_data(*args, **kwargs)
        context['value'] = (self.kwargs.get("test"))
        print(self.request.GET)
        print(self.kwargs)
        return context


# Организация поиска
# 1. Вариант
class SearchBooks(ListView):
    template_name = 'books/book_list.html'

    def get_queryset(self):
        val = self.kwargs.get("urlsearch")
        if val:
            queryset = Book.objects.filter(title__icontains=val)
        else:
            queryset = Book.objects.none()
        return queryset


# 2. Вариант
class QSearchBooks(ListView):
    template_name = 'books/book_list.html'

    def get_queryset(self):
        val = self.kwargs.get('qurlsearch')
        if val:
            queryset = Book.objects.filter(
                Q(title__contains=val) |
                Q(authors__first_name__icontains=val)
            )
            queryset = queryset.distinct()  # убираем повторы в выдаче, если у книги окажется несолько авторов
        else:
            queryset = Book.objects.none()
        return queryset


# Link to search form
class BookSearch(TemplateView):
    template_name = 'books/search_form.html'


class BookSearchResult(ListView):
    model = Book
    template_name = 'books/book_list.html'

    def get_queryset(self, *args, **kwargs):
        print(self.request)
        val = self.request.GET.get("q")
        print(val)
        if val:
            queryset = Book.objects.filter(
                Q(title__icontains=val) |
                Q(content__icontains=val)
            ).distinct()
        else:
            queryset = Book.objects.none()
        print(queryset)
        return queryset

# Model Forms


def author_create(request):
    form = AuthorForm(request.POST or None)
    error = None
    if form.is_valid():
        # Если нужно сразу сохранить данные формы
        # form.save()
        # Если нужно сделать какие-либо операции, то так:
        new_item = form.save(commit=False)
        context = {
            "item": "Author",
            "title": new_item.first_name,
        }
        new_item.save()
        template_name = 'books/thanks_create.html'
        return render(request, template_name, context)
    else:
        errors = form.errors
        template_name = 'books/create_form.html'
        context = {
            "form": form,
            "errors": errors,
            "item": "Author"
        }
        return render(request, template_name, context)


class AuthorList(ListView):
    # # default template location : lowercaseAppName/lowercaseAppName_list.html
    # template_name = "books/book_list.html"

    # by default 'queryset' is sent as context
    queryset = Author.objects.all()  # 'queryset' is reserved name like 'template_name'

    # to pass more context, inherit cotext with 'super' and
    # then include the items in the context  using 'get_context_data'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["name"] = "Harry"
        return context
