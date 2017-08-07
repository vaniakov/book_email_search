from book_search.tests import TestCase
from books.models import Book


class BookSearchModelsTestCase(TestCase):
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

    def test_find_for_query_exists(self):
        result = Book.find_for_query('hello')
        self.assertEqual(len(result['matches']), 1)
        self.assertEqual(result['matches'][0]['title'], 'Test')
        self.assertEqual(result['matches'][0]['page'], 1)
