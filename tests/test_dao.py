import unittest
import logging

# from dao import DatabaseDao
# from settings import SaaeSettings
from util import Util


class TestDatabaseDao(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO, format=Util.LOG_FORMAT_FULL)
        # self.settings = SaaeSettings('.env')

    def test_dao(self):
        self.fail('TODO implement it!')
        # result = None

        # query = """
        #             SELECT
        #                 j.id_job
        #             FROM gecon.job AS j
        #             WHERE
        #                 j.id_job = 1
        #             ;"""

        # with DatabaseDao(settings=self.settings) as dao:
        #     dao.cursor.execute(query)
        #     query_result = dao.cursor.fetchone()

        #     if query_result is not None:
        #         result = query_result[0]

        # self.assertIsNotNone(result)
        # self.assertEqual(result, 1)
