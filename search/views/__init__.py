from drf_yasg import openapi
from rest_framework import status


download_invitee_response_schema_dict = {
    status.HTTP_200_OK: openapi.Response(
        description='초대자/피초대자 목록',
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'invitee_info': openapi.Schema(type=openapi.TYPE_OBJECT,
                                               description='초대 타입 : '
                                                           'invite_type (0 : 초대자), '
                                                           'ID: id, '
                                                           '이름: name, '
                                                           '이메일: email, '
                                                           '생년월일 : birth, '
                                                           '번호: phone, '
                                                           '회사: company, '
                                                           '사번: employee_num, '
                                                           '초대코드: join_code, '
                                                           '초대한 친구 수 : invited_friends_count '
                                               ),
                'invited_info': openapi.Schema(type=openapi.TYPE_OBJECT,
                                               description='초대 타입 : invite_type (1: 피초대자), '
                                                           'ID: id, '
                                                           '이름: name, '
                                                           '이메일: email, '
                                                           '생년월일 : birth, '
                                                           '번호: phone, '
                                                           '회사: company, '
                                                           '사번: employee_num, '
                                                           '초대코드: join_code, '
                                                           '가입일 : reg_date, '
                                                           '첫 인출일 : first_withdrawal_date, '
                                                           '인출 금액: withdrawal_amount '
                                               )})),
}