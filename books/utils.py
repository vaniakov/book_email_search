from django.core.mail import send_mail


def format_result(result):
    """Format search result into email text.

    :param result: dict in format: {time: 0, query: 'query', matches:
                  [{title: 'title', 'author': 'author', year: 2014,
                    page: 22, text: 'page text']}
    :return: string with formatted result.
    """
    header = 'Results for query "{0}". Matches found: {1}\n'.format(
        result['query'], len(result['matches']))
    message = [header]
    template = "Book: {author} - {title} - {year}\nPage: {page}\nText: {text}\n"
    for match in result['matches']:
        message.append(template.format(**match))
    footer = '\nSearch took {0} seconds'.format(result['time'])
    message.append(footer)
    return (80 * '-') + '\n'.join(message)


def extract_sentence_from_page(query, page):
    """Extract sentences that match provided query from page text.

    :param query: Pattern to find.
    :param page: Page text.
    :return: string with sentences that match provided query in the page.
    """
    result = []
    sentances = page.split('.')
    for sentance in sentances:
        if query in sentance:
            result.append(sentance)
    return ' ..... '.join(result)


def send_result_email(to, query, search_result):
    """Send email with results to requester of the search.

    :param to: email address of the requester.
    :param query: query string.
    :param search_result: dict with results(see format_results func).
    """
    subject = 'Results for your query: "{0}"'.format(query)
    sender = 'noreply@book_search.com'
    message = format_result(search_result)
    recipients = [to]
    send_mail(subject, message, sender, recipients)