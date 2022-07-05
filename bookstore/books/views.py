from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

#



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
