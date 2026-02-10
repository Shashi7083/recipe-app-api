"""
Test custom Django management commands.
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
#  possible error that we might get

from django.core.management import call_command
#  may get through database
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
#  to mock behaviour of DB
class TestCommands(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        #  patched_check object is passed in function
        """Test waiting for database if database ready"""

        patched_check.return_value = True

        call_command('wait_for_db')
        #  this will execute the code inside DB

        patched_check.assert_called_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        #  keep order correct for time.sleep it will take
        #  first object then class patch (bottom to top order)
        """Test waiting for database when getting Operational Error."""

        #  first two time raise Psycopg2Error and then
        #  3 times raise OperationalError then return true
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
