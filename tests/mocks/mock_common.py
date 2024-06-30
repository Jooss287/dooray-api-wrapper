import re
from tests.mocks.const import host, success_response_header
from tests.mocks.structure import MockResponse


def mocked_get_request_success(*args, **kwargs):
    api = [
        (
            # GET /common/v1/members
            re.compile(host + r"/common/v1/members"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": [
                        {
                            "id": "{id}",
                            "name": "{name}",
                            "userCode": "",
                            "externalEmailAddress": "{extenralEmailAddress}",
                        }
                    ],
                    "totalCount": 1,
                },
                200,
            ),
        ),
        (
            # GET /common/v1/members/{member-id}
            re.compile(host + r"/common/v1/members/\d+"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": {
                        "id": "userIdSample",
                        "idProviderType": "sso",
                        "idProviderUserId": "",
                        "name": "",
                        "userCode": "",
                        "externalEmailAddress": "",
                        "defaultOrganization": {"id": ""},
                        "locale": "",
                        "timezoneName": "",
                        "englishName": "",
                        "nativeName": "",
                        "nickname": "",
                        "displayMemberId": "",
                    },
                },
                200,
            ),
        ),
    ]

    for item in api:
        if item[0].fullmatch(args[0]):
            return item[1]

    return MockResponse(None, 404)
