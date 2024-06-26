class MockResponse:
    def __init__(self, json_data, status_code, from_cache=False):
        self.json_data = json_data
        self.status_code = status_code
        self.from_cache = from_cache

    def json(self):
        return self.json_data
