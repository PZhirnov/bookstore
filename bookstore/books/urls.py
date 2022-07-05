from django.urls import path
from .views import fexample, http_example, CExample

urlpatterns = [
    path('httpExample/', http_example, name='http_example'),  # HttpResponse
    path('fexample/', fexample, name='fexample'),  # function-based-view
    path('cexample/', CExample.as_view(), name='cexample'),  # class-based-view
]




