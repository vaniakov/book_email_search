from unittest.mock import patch
from django.test import Client
from django.core.urlresolvers import reverse

from book_search.tests import TestCase
from books.models import Book
from books.forms import IndexForm
from books import utils


class BookSearchTestCase(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test',
            'author': 'Test Author',
            'year': 2017,
            'pages': [
                {
                    'page_num': 1,
                    'text': 'About unicorn corn. \nFind trouble. \nhello.'
                },
                {
                    'page_num': 2,
                    'text': 'green grass. violence is everywhere. bad dream.'
                },
            ]
        }
        self.book_data2 = {
            'title': 'Pro Python',
            'author': 'M. Alchin',
            'year': 2012,
            'pages': [
                {
                    'page_num': 1,
                    'text': 'About author'
                },
                {
                    'page_num': 2,
                    'text': 'Python is awesome.'
                },
            ]
        }
        self.book_obj = Book.objects.create(**self.book_data)
        self.book_obj2 = Book.objects.create(**self.book_data2)

    def tearDown(self):
        Book.objects.all().delete()


class FindForQueryTests(BookSearchTestCase):
    def test_find_for_query_exists(self):
        result = Book.find_for_query('hello')
        self.assertEqual(len(result['matches']), 1)
        self.assertEqual(result['matches'][0]['title'], 'Test')
        self.assertEqual(result['matches'][0]['page'], 1)

    def test_find_for_query_not_exists(self):
        result = Book.find_for_query('Not exists')
        self.assertEqual(len(result['matches']), 0)

    def test_find_for_query_multiple_match(self):
        result = Book.find_for_query('About')
        self.assertEqual(len(result['matches']), 2)
        self.assertEqual(result['matches'][0]['title'], 'Test')
        self.assertEqual(result['matches'][1]['title'], 'Pro Python')


class BooksUtilsTestCase(BookSearchTestCase):
    def test_extract_results(self):
        result = Book.find_for_query('hello')
        formatted = utils.format_result(result)
        self.assertTrue(
            'Results for query "hello". Matches found: 1' in formatted)

    def test_extract_sentence_from_page(self):
        page = 'One test. Two test. Three unicorn. Four unicorn'
        result = utils.extract_sentence_from_page('unicorn', page)
        self.assertEqual(result, ' Three unicorn .....  Four unicorn')

    @patch('books.utils.send_mail')
    def test_send_result_email(self, send_email_mock):
        result = Book.find_for_query('hello')
        message = utils.format_result(result)
        subject = 'Results for your query: "hello"'
        sender = 'noreply@book_search.com'
        utils.send_result_email('test@email.com', 'hello', result)
        send_email_mock.assert_called_once_with(subject, message, sender,
                                                ['test@email.com'])


class ViewsTests(BookSearchTestCase):
    def test_index_view_response_get_200(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_post_redirect(self):
        client = Client()
        response = client.post(reverse('index'), {'email': 'test@test.com',
                                                  'query': 'python'})
        self.assertEqual(response.status_code, 302)

    def test_index_view_post_redirect_result(self):
        client = Client()
        response = client.post(reverse('index'), {'email': 'test@test.com',
                                                  'query': 'python'},
                               follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['email'], 'test@test.com')
        self.assertEqual(response.context[-1]['query'], 'python')

    def test_results_view_redirect_302(self):
        client = Client()
        response = client.get(reverse('success_request'))
        self.assertEqual(response.status_code, 302)

    def test_results_view_redirect_200(self):
        client = Client()
        response = client.get(reverse('success_request'), follow=True)
        self.assertEqual(response.status_code, 200)


class FormTests(TestCase):
    def test_form_without_limit(self):
        form = IndexForm({'email': 'test@test.com', 'query': 'python'})
        form_valid = form.is_valid()
        self.assertEqual(form.cleaned_data['email'], 'test@test.com')
        self.assertTrue(form_valid)

    def test_form_valid_with_limit(self):
        form = IndexForm({'email': 'test@test.com', 'query': 'python',
                          'time_limit': 120})
        form_valid = form.is_valid()
        self.assertEqual(form.cleaned_data['time_limit'], 120)
        self.assertTrue(form_valid)

    def test_form_empty_email(self):
        form = IndexForm({'email': '', 'query': 'python'})
        form_valid = form.is_valid()
        self.assertFalse(form_valid)

    def test_form_empty_query(self):
        form = IndexForm({'email': 'test@test.com', 'query': ''})
        form_valid = form.is_valid()
        self.assertFalse(form_valid)