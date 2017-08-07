import logging
import mongoengine
import time

from books.utils import extract_sentence_from_page

logger = logging.getLogger(__name__)


class Page(mongoengine.EmbeddedDocument):
    """Database page representation."""
    page_num = mongoengine.IntField()
    text = mongoengine.StringField()


class Book(mongoengine.Document):
    """Database book representation."""
    title = mongoengine.StringField(max_length=200)
    author = mongoengine.StringField(max_length=200)
    year = mongoengine.IntField()
    pages = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Page))

    @classmethod
    def find_for_query(cls, query, limit_seconds=None):
        """Looks for query in all books.
        Search time can be limited by `limit_seconds` param.

        :param query: String to search.
        :param limit_seconds: Limit search time in seconds.
        """
        result = {'time': 0, 'matches': [], 'query': query}
        start = time.time()
        logger.info('Starting search...')
        for book in cls.objects.all():
            for page in book.pages:
                if query in page.text:
                    match = {
                        'title': book.title,
                        'author': book.author,
                        'year': book.year,
                        'page': page.page_num,
                        'text': extract_sentence_from_page(query, page.text)
                    }
                    result['matches'].append(match)
                if limit_seconds and start + limit_seconds <= time.time():
                    logger.info('Finished search because of timeout(%s)!',
                                limit_seconds)
                    result['time'] = time.time() - start
                    return result
        logger.info('Finished search, match found on %s pages!', len(result['matches']))
        result['time'] = time.time() - start
        return result
