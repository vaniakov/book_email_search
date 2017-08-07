from django.views.generic import FormView, TemplateView
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy

from books.forms import IndexForm
from books.tasks import search_for_query

# flush cookie with request data after(seconds)
COOKIE_EXPIRE = 5


class IndexView(FormView):
    """Main page. Responsible for displaying query form.

    Stores intermediate data in the cookie storage."""
    form_class = IndexForm
    success_url = reverse_lazy('success_request')
    template_name = 'index.html'

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        search_for_query.delay(**cleaned_data)
        response = super().form_valid(form)
        response.set_cookie('email', cleaned_data['email'], COOKIE_EXPIRE)
        response.set_cookie('query', cleaned_data['query'], COOKIE_EXPIRE)
        response.set_cookie('limit', cleaned_data['time_limit'], COOKIE_EXPIRE)
        return response


class SuccessRequestView(TemplateView):
    """Page to display when user sent query request."""
    template_name = 'request_success.html'

    def get(self, request, *args, **kwargs):
        if not request.COOKIES.get('email'):
            return HttpResponseRedirect(reverse_lazy('index'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        cookies = self.request.COOKIES
        context_data['email'] = cookies.get('email')
        context_data['query'] = cookies.get('query')
        context_data['time_limit'] = cookies.get('limit')
        return context_data
