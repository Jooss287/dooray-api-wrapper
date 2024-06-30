import unittest
from unittest.mock import patch
import src.dooray_api_wrapper.dooray.common as dooray_common
from tests.mocks.mock_common import mocked_get_request_success


class TestCommon(unittest.TestCase):

    def test_get_member_list(self):
        with patch("requests.get", side_effect=mocked_get_request_success):
            result = dooray_common.get_members("test@gmail.com")

            self.assertIsNotNone(result)

    def test_get_member_info(self):
        with patch("requests.get", side_effect=mocked_get_request_success):
            result = dooray_common.get_member_info("1231467")

            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
