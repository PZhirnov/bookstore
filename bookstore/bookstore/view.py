from django.shortcuts import render


def all_links(request):
    return render(request, 'bookstore/all_links.html')
