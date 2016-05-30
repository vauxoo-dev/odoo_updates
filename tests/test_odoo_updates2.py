from unittest import TestCase
import testing.postgresql
from odoo_updates import odoo_updates
import mock

def mocked_exec_select(*args, **kwargs):
    return [{'xml_id': 1}, {'xml_id': 2}]


class TestOdooUpdates(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgresql = testing.postgresql.Postgresql()

    @mock.patch('odoo_updates.utils.PostgresConnector.execute_select',
                side_effect=mocked_exec_select)
    def test_01_menu_tree(self, mocked):
        res = odoo_updates.menu_tree(1, self.postgresql.dsn())
        self.assertIsInstance(res, dict)
        self.assertEquals(res, mocked_exec_select()[0])

    @mock.patch('odoo_updates.utils.PostgresConnector.execute_select',
                side_effect=mocked_exec_select)
    def test_02_get_menus(self, mocked):
        res = odoo_updates.get_menus(self.postgresql.dsn())
        self.assertIsInstance(res, dict)

    @mock.patch('odoo_updates.utils.PostgresConnector.execute_select',
                side_effect=mocked_exec_select)
    def test_03_get_views(self, mocked):
        res = odoo_updates.get_views(self.postgresql.dsn())
        self.assertIsInstance(res, list)
        self.assertTrue(res)
