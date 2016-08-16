from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('params1', nargs='?', type=str)

    def handle(self, *args, **options):
        # Using parameters:
        param1 = options['params1']
        self.stdout.write('[#] Begin execute...')
        try:
            if param1:
                self.stdout.write('[#] Hello ' + str(param1))
            else:
                self.stdout.write('[#] Hello World')
        except Exception as e:
            print('Error:', e)
        self.stdout.write('[#] DONE!')
