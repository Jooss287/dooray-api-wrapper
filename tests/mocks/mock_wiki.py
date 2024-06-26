import re
from tests.mocks.const import host, success_response_header
from tests.mocks.structure import MockResponse


def mocked_get_request_success(*args, **kwargs):
    api = [
        (
            # GET /wiki/v1/wikis
            re.compile(host + r"/wiki/v1/wikis"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": [
                        {
                            "id": "100",
                            "project": {"id": "10"},
                            "name": "Dooray-공지사항",
                            "type": "public",
                            "scope": "public",
                            "home": {"pageId": "1001"},
                        }
                    ],
                    "totalCount": 1,
                },
                200,
            ),
        ),
        (
            # GET /wiki/v1/wikis/{wikiId}/pages
            re.compile(host + r"/wiki/v1/wikis/\d+/pages"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": [
                        {
                            "id": "100",
                            "wikiId": "1",
                            "version": "2",
                            "parentPageId": "10",
                            "subject": "공지사항",
                            "root": True,
                            "creator": {
                                "type": "member",
                                "member": {
                                    "organizationMemberId": "2139624229289676300"
                                },
                            },
                        }
                    ],
                },
                200,
            ),
        ),
        (
            # GET /wiki/v1/wikis/{wikiId}/pages/{pageId}
            re.compile(host + r"/wiki/v1/wikis/\d+/pages/\d+"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": {
                        "id": "100",
                        "wikiId": "1",
                        "version": 2,  # api doc에는 str이나 실제로는 int
                        "parentPageId": "10",
                        "subject": "공지사항",
                        "body": {
                            "mimeType": "text/x-markdown",
                            "content": "위키 본문 내용",
                        },
                        "root": True,
                        "createdAt": "2019-08-08T16:58:27+09:00",
                        "creator": {
                            "type": "member",
                            "member": {
                                "organizationMemberId": "2139624229289676300",
                            },
                        },
                        "referrers": [
                            {"type": "member", "member": {"organizationMemberId": ""}}
                        ],
                        "files": [{"id": "1390"}],
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


def mocked_post_request_success(*args, **kwargs):
    api = [
        (
            re.compile(host + r"/wiki/v1/wikis/\d+/pages"),
            MockResponse(
                {
                    "header": success_response_header,
                    "result": {
                        "id": "100",
                        "wikiId": "1",
                        "parentPageId": "10",
                        "version": 2,
                    },
                },
                200,
            ),
        ),
    ]

    for item in api:
        if item[0].match(args[0]):
            return item[1]

    return MockResponse(None, 404)


def mocked_put_request_success(*args, **kwargs):
    api = [
        (
            re.compile(host + r"/wiki/v1/wikis/\d+/pages/\d+"),
            MockResponse(
                {"header": success_response_header, "result": None},
                200,
            ),
        ),
        (
            re.compile(host + r"/wiki/v1/wikis/\d+/pages/\d+/title"),
            MockResponse(
                {"header": success_response_header, "result": None},
                200,
            ),
        ),
        (
            re.compile(host + r"/wiki/v1/wikis/\d+/pages/\d+/content"),
            MockResponse(
                {"header": success_response_header, "result": None},
                200,
            ),
        ),
        (
            re.compile(host + r"/wiki/v1/wikis/\d+/pages/\d+/referrers"),
            MockResponse(
                {"header": success_response_header, "result": None},
                200,
            ),
        ),
    ]

    for item in api:
        if item[0].match(args[0]):
            return item[1]

    return MockResponse(None, 404)
