import unittest
from unittest.mock import patch
import src.dooray_api_wrapper.dooray.wiki as dooray_wiki
from tests.mocks.mock_wiki import (
    mocked_get_request_success,
    mocked_post_request_success,
)


class TestWiki(unittest.TestCase):

    def test_get_wiki_list(self):
        with patch("requests.get", side_effect=mocked_get_request_success):
            result = dooray_wiki.get_wiki_list()

            self.assertIsNotNone(result)

    def test_get_wiki_sub_pages(self):
        with patch("requests.get", side_effect=mocked_get_request_success):
            result = dooray_wiki.get_wiki_sub_pages("100")

            self.assertIsNotNone(result)

    def test_get_wiki_page(self):
        with patch("requests.get", side_effect=mocked_get_request_success):
            result = dooray_wiki.get_wiki_page("100", "100")

            self.assertIsNotNone(result)

    def test_create_wiki_page(self):
        with patch("requests.post", side_effect=mocked_post_request_success):
            result = dooray_wiki.create_wiki_page("100", "100", "title", "content")

            self.assertIsNotNone(result)

    def test_edit_wiki_page(self):
        with patch("requests.put", side_effect=mocked_post_request_success):
            result = dooray_wiki.edit_wiki_page("100", "100", "title", "content")

            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
