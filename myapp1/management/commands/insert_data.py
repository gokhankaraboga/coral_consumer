from django.core.management.base import BaseCommand
from myapp1.models import Destination, Hotel
import csv


class Command(BaseCommand):
    help = 'Command to insert static hotel and destination data the db'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

        # destination for destination data, hotel for hotel data

    def handle(self, *args, **options):
        filename = options.get('file_path')

        if 'destination' in options.get('file_path'):
            copy_class = Destination

        elif 'hotel' in options.get('file_path'):
            copy_class = Hotel

        try:
            with open(filename) as f:
                csvread = csv.reader(f, delimiter=',')

                for row in csvread:
                    if row[0] not in copy_class.objects.values_list(
                            'coral_code',
                            flat=True):
                        copy_class.objects.create(coral_code=row[0],
                                                  name=row[1])
                    else:
                        return 'Duplicate Record has been detected'
        except IOError as detail:
            print 'Unexpected Database Error', detail
