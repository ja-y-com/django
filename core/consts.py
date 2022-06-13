KAKAO_CHAT_BOT_DEFAULT_LIST_CARD_MESSAGE = {
    "version": "2.0",
    "template": {
        "outputs": [
            {"listCard": {"header": {"title": ""}, "items": [], "buttons": []}}
        ],
        "quickReplies": [],
    },
}

KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE = {
    "version": "2.0",
    "template": {"outputs": [{"simpleText": {"text": ""}}], "quickReplies": []},
}

KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE_FORMAT = {
    "object_type": "text",
    "text": "",
    "link": {"web_url": "", "mobile_web_url": ""},
}

# 통합 검색
SEARCH_MEMBER_KEYWORDS = [
    "name",  # 이름
    "age",  # 나이
    "gender",  # 성별
    "phone_number",  # 휴대폰 번호
    "c_alone",  # 사용자만 가입
    "register_date"  # 가입일
    "last_login_date",  # 마지막 로그인
    "invitee_join_date",  # 친구 가입일
    "invitee_first_withdraw_date",  # 친구 첫 인출일
]
SEARCH_COMPANY_KEYWORDS = [
    "company_name",  # 기업명
    "company_type",  # 기업 형태
    "company_user_qty",  # 소속 사용자 수
    "company_create_date",  # 기업 생성일
]
SEARCH_MEMBER_PAIR_KEYWORDS = [
    "pay_date",  # 급여일
    "join_date",  # 입사일
    "left_date",  # 퇴사일
]
SEARCH_MILEAGE_KEYWORDS = [
    "miles_balance",  # 보유 마일리지
    "miles_auto_pay_start_date",  # 마일리지 자동지급 시작일
]
SEARCH_WORK_KEYWORDS = [
    "work_number_of_time",  # 출퇴근 횟수
    "last_work_date",  # 마지막 퇴근일
]
SEARCH_ADVANCE_PAYMENT_KEYWORDS = [
    "adv_prod",  # 선지급 상품
    "adv_appd_date",  # 선지급 승인일
    "adv_exp_date",  # 선지급 만료일
    "adv_repay_date",  # 선지급 실제 상환일
    "adv_use_qty",  # 선지급 사용 횟수
    "adv_use_amt",  # 선지급 사용 금액
    "contract_status",  # 계약 상태
    "seperate_transfer_status",  # 분리이체 상태
    "repay_method",  # 상환 방법
    "repay_date_range",  # 상환일 범위
]
