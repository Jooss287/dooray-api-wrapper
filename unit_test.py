import sys, os

module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
print(module_path)
sys.path.append(module_path)

import unittest
from dotenv import load_dotenv

load_dotenv(override=True)


def run_tests():
    # TestLoader를 사용하여 현재 디렉토리의 모든 테스트를 발견
    loader = unittest.TestLoader()

    suite = unittest.TestSuite()
    suite.addTest(loader.discover("tests", pattern="test_*.py"))

    # 테스트 러너 실행
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    run_tests()
