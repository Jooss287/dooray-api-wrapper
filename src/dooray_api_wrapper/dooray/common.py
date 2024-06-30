from typing import List, Union, Dict, Optional

from dooray_api_wrapper.common import dooray_request
from dooray_api_wrapper.structure import response_result, response_header


def get_members(
    external_email_address: str,
    *,
    name: Optional[str] = None,
    userCode: Optional[str] = None,
    idProviderUserId: Optional[str] = None,
):
    """
    GET /common/v1/members
    멤버 목록을 조회합니다.
    external_email_address는 정확히 일치해야 합니다.
    """

    end_point = f"/common/v1/members"
    params = {
        "externalEmailAddress": external_email_address,
        "name": name,
        "userCode": userCode,
        "idProviderUserId": idProviderUserId,
    }

    data = dooray_request.dooray_get(end_point, params)
    if data is None:
        return None

    def response(
        data: Dict,
    ) -> Optional[
        List[Union[response_header.ResponseHeader, response_result.MemberResult]]
    ]:
        if "header" not in data or "result" not in data:
            return None

        header = response_header.ResponseHeader(**data["header"])
        result = {"result": data["result"]}
        return [header, response_result.MemberResult(**result)]

    [header, member_list] = response(data)
    cnt = len(member_list.result)
    if "totalCount" not in data:
        return member_list

    total_count = data["totalCount"]

    while cnt < total_count:
        params["page"] += 1
        data = dooray_request.dooray_get(end_point, params)
        if data is None:
            return member_list

        [header, result] = response(data)
        member_list.result.extend(result.result)
        cnt = len(member_list.result)

    return member_list


def get_member_info(member_id: str) -> Optional[response_result.MemberResultItem]:
    """
    GET /common/v1/members/{memberId}
    멤버 정보를 조회합니다.
    """

    end_point = f"/common/v1/members/{member_id}"
    response = dooray_request.dooray_get(end_point)
    if response is None:
        return None

    header = response["header"]
    result = {"result": response["result"]}
    return result
