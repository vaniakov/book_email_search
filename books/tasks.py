# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task import task
from celery.utils.log import get_task_logger

from books.models import Book
from books.utils import send_result_email, format_result

logger = get_task_logger(__name__)


@task(name="search_for_query")
def search_for_query(query, email, time_limit):
    """Looking for query in all books stored in database.
    In the end of search sent an email with results.

    :param query: Query to look for.
    :param email: Email to send results to.
    :param time_limit: Limit query in time(seconds).
    """
    logger.info("Search started...")
    result = Book.find_for_query(query, time_limit)
    logger.info('Search finished!')
    send_result_email(email, query, result)
    logger.info('Message to %s has been sent!', email)
