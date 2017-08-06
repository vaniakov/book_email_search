import logging
import os
import time
import glob

from PyPDF2 import PdfFileReader
from django.core.management.base import BaseCommand, CommandError

from books.models import Book


class Command(BaseCommand):
    help = 'Export pdf book(s) from given source.'

    def add_arguments(self, parser):
        parser.add_argument('source', nargs='+', type=str)

    def handle(self, *args, **options):
        pdf_files = self._clear_options(options)
        pdf_book_parser = PdfBookParser()
        created = []
        for file_path in pdf_files:
            book_info = pdf_book_parser._parse_book_info(file_path)
            book_exists = bool(
                Book.objects.filter(title=book_info.get('title'),
                                    author=book_info.get('author'),
                                    year=book_info.get('year')))
            basename = os.path.basename(file_path)
            if book_exists:
                self.stdout.write(self.style.ERROR(
                    'Book "{}" already exists. Skipping..'.format(
                        basename)))
            else:
                try:
                    parsed_data = pdf_book_parser.parse(file_path)
                    created.append(Book.objects.create(**parsed_data))
                except Exception as err:
                    self.stdout.write(
                        self.style.ERROR('Unable to create book {}: {}'.format(
                            basename, err
                        )))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        'Successfully added {} to database'.format(basename)))
        if len(created) > 0:
            self.stdout.write(self.style.SUCCESS(
                'Successfully added {} books to database'.format(len(created))))

    def _clear_options(self, options):
        pdf_files = options['source']
        source = options['source'][0]
        if os.path.isdir(source):
            pdf_files = glob.glob(os.path.join(source, '*.pdf'))
        elif not source.endswith('.pdf'):
            raise CommandError('Provided file have to be in .PDF format.')
        return pdf_files


class PdfBookParser(object):
    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    def _parse_pages(self, book_path):
        result = []
        start = time.time()
        with open(book_path, 'rb') as fh:
            input_pdf = PdfFileReader(fh)
            self._log.info('Start processing %s with %s pages...', book_path,
                           input_pdf.getNumPages())
            if input_pdf.flattenedPages is None:
                input_pdf._flatten()
            for page_num, page in enumerate(input_pdf.flattenedPages, start=1):
                result.append(
                    {'page_num': str(page_num), 'text': page.extractText()})
        self._log.info('Finished processing %s in %s seconds.', book_path,
                       time.time() - start)
        return result

    def _parse_book_info(self, book_path):
        author, title_with_ext = os.path.basename(book_path).split(' - ', 1)
        title = title_with_ext.rsplit('.', 1)[0]
        year = None
        if '-' in title:
            title, year = title.rsplit('-', 1)
            year = int(year)
        return {'author': author, 'title': title, 'year': year}

    def parse(self, book_path):
        book = self._parse_book_info(book_path)
        book['pages'] = self._parse_pages(book_path)
        return book
