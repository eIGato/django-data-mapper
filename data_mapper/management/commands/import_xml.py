"""Management command to import data from XML file to database."""
from django.core.management.base import BaseCommand

from data_mapper import XmlMapper


class Command(BaseCommand):
    help = 'Import data from XML file to database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            help='XML file name to import data from.'
        )

    def handle(self, *args, **kwargs):
        xml_mapper = XmlMapper(kwargs['filename'])
        xml_mapper.import_data()
