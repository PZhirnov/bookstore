from django.urls import path, re_path
from .views import fexample, http_example, CExample, \
    book_list, BookList, BookDetail, read_arg, read_kwarg, ReadArg, ReadKwarg, SearchBooks, QSearchBooks

app_name = 'books'

urlpatterns = [
    path('httpExample/', http_example, name='http_example'),  # HttpResponse
    path('fexample/', fexample, name='fexample'),  # function-based-view
    path('cexample/', CExample.as_view(), name='cexample'),  # class-based-view
    path('fbooklist/', book_list, name='fbooklist'),
    re_path(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='bookdetail'),
    re_path(r'^$', BookList.as_view(), name='booklist'),
    re_path(r'^freadargs/(\w+)/$', read_arg, name='freadargs'),
    re_path(r'^freadkwargs/(?P<test>\w+)/$', read_kwarg, name='freadkwargs'),
    re_path(r'^readargs/(\w+)/$', ReadArg.as_view(), name='readargs'),
    re_path(r'^readkwargs/(?P<test>\w+)/$', ReadKwarg.as_view(), name='readkwargs'),
    re_path(r'^searchfromurl/(?P<urlsearch>[\w-]+)/$', SearchBooks.as_view(), name="searchfromurl"), # search item received from url
    re_path(r'^qsearchfromurl/(?P<qurlsearch>[\w-]+)/$', QSearchBooks.as_view(), name="qsearchfromurl"),
]






