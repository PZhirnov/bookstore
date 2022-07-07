from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import Book

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
    print(request.GET)
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

