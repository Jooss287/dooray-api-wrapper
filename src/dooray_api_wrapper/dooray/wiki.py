from typing import Dict, List, Union, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.structure import response_result, response_header
from dooray_api_wrapper.const.const import ContentType


def get_wiki_list() -> Optional[response_result.WikiResult]:
    """
    GET /wiki/v1/wikis
    접근 가능한 위키 목록을 조회합니다.
    """
    end_point = f"/wiki/v1/wikis"
    params = {
        "page": 0,
        "size": 100,
    }

    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    def response(
        data: Dict,
    ) -> Optional[
        List[Union[response_header.ResponseHeader, response_result.WikiResult]]
    ]:
        if "header" not in data or "result" not in data:
            return None

        header = response_header.ResponseHeader(**data["header"])
        result = {"result": data["result"]}
        return [header, response_result.WikiResult(**result)]

    [header, wiki_list] = response(data)
    cnt = len(wiki_list.result)
    if "totalCount" not in data:
        return wiki_list

    total_count = data["totalCount"]

    while cnt < total_count:
        params["page"] += 1
        data = dooray_request.dooray_get(end_point, params)
        if data is None:
            return wiki_list

        [header, result] = response(data)
        wiki_list.result.extend(result.result)
        cnt = len(wiki_list.result)

    return wiki_list


def get_wiki_sub_pages(
    wiki_id: str, *, parentPageId: Optional[str] = None
) -> Optional[response_result.WikiPageResult]:
    """
    GET /wiki/v1/wikis/{wikiId}/pages
    특정 위키 페이지의 하위 페이지들을 조회합니다.

    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages"
    params = {
        "parentPageId": parentPageId,
    }
    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    header = data["header"]
    result = {"result": data["result"]}
    return response_result.WikiPageResult(**result)


def get_wiki_page(
    wiki_id: str, pageId: str
) -> Optional[response_result.WikiPageResultItem]:
    """
    GET /wiki/v1/wikis/{wikiId}/pages/{pageId}
    특정 위키 페이지를 조회합니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{pageId}"
    response = dooray_request.dooray_get(end_point)
    if response is None:
        return None

    header = response["header"]
    result = response["result"]
    return response_result.WikiPageResultItem(**result)


def create_wiki_page(
    wiki_id: str,
    parentPageId: str,
    title: str,
    content: str,
    *,
    content_type: ContentType = ContentType.MARKDOWN,
    attach_files: List[str] = [],
    referrers: List[str] = [],
) -> Optional[response_result.WikiPageResultItem]:
    """
    POST /wiki/v1/wikis/{wikiId}/pages
    위키 페이지를 생성합니다.
    * 본문은 markdown 형식으로 처리됩니다
    * referrers 필드는 위키의 참조자입니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages"

    data = {
        "parentPageId": parentPageId,
        "subject": title,
        "body": {
            "mimeType": content_type.value,
            "content": content,
        },
        "attachFileIds": attach_files,
        "referrers": [
            {"type": "member", "member": {"organizationMemberId": member_id}}
            for member_id in referrers
        ],
    }
    response = dooray_request.dooray_post(end_point, data)
    if response is None:
        return None

    header = response["header"]
    result = response["result"]
    return response_result.WikiPageResultItem(**result)


def edit_wiki_page(
    wiki_id: str,
    page_id: str,
    subject: str,
    content: str,
    *,
    content_type: ContentType = ContentType.MARKDOWN,
    referrers: List[str] = [],
) -> bool:
    """
    PUT /wiki/v1/wikis/{wikiId}/pages/{pageId}
    위키 페이지를 수정합니다.
    * referrers는 기존의 참조자를 덮어씁니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{page_id}"

    data = {
        "subject": subject,
        "body": {
            "mimeType": content_type,
            "content": content,
        },
        "referrers": [
            {"type": "member", "member": {"organizationMemberId": member_id}}
            for member_id in referrers
        ],
    }
    response = dooray_request.dooray_put(end_point, data)
    if response is None:
        return False

    return True


def edit_wiki_page_title(
    wiki_id: str,
    page_id: str,
    subject: str,
) -> bool:
    """
    PUT /wiki/v1/wikis/{wikiId}/pages/{pageId}/title
    위키 페이지 제목을 수정합니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{page_id}"

    data = {"subject": subject}
    response = dooray_request.dooray_put(end_point, data)
    if response is None:
        return False

    return True


def edit_wiki_page_content(
    wiki_id: str,
    page_id: str,
    content: str,
    *,
    content_type: ContentType = ContentType.MARKDOWN,
) -> bool:
    """
    PUT /wiki/v1/wikis/{wikiId}/pages/{pageId}/content
    위키 페이지 내용을 수정합니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{page_id}"

    data = {"mimeType": content_type, "content": content}
    response = dooray_request.dooray_put(end_point, data)
    if response is None:
        return False

    return True


def edit_wiki_page_referrers(
    wiki_id: str, page_id: str, referrers: List[str] = []
) -> bool:
    """
    PUT /wiki/v1/wikis/{wikiId}/pages/{pageId}/referrers
    위키 페이지 참조자를 수정합니다.
    """
    end_point = f"/wiki/v1/wikis/{wiki_id}/pages/{page_id}/referrers"

    data = [
        {"type": "member", "member": {"organizationMemberId": member_id}}
        for member_id in referrers
    ]
    response = dooray_request.dooray_put(end_point, data)
    if response is None:
        return False

    return True
