from backend.apps.lexxer.generate.myth.syn import MythSyntax
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Console mode for Mythos"

    def handle(self, *args, **options):
        syntax = MythSyntax()

        while True:
            try:
                s = input('MYTH >>')
                if not s: continue
            except EOFError: break
            result = syntax.test(s)
            print(result)
