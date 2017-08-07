"""book_search URL Configuration."""
from django.conf.urls import url

from books.views import IndexView, SuccessRequestView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^success/$', SuccessRequestView.as_view(), name='success_request'),
]
