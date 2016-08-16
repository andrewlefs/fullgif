from django.core.management.base import BaseCommand

from ... import auto_9gag


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('params1', nargs='?', type=int)

    def handle(self, *args, **options):
        # Using parameters:
        # print('params1:', options['params1']
        self.stdout.write('[#] Begin execute...')
        try:
            auto = auto_9gag.AutoNews()
            auto.run()
        except Exception as e:
            print('Error:', e)
        self.stdout.write('[#] DONE!')