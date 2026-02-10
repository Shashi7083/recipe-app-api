"""
Django command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError
import time

from django.db.utils import OperationalError
from django.test import SimpleTestCase


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                #  it will throw exception when database is not ready
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
