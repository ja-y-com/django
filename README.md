# API Server
> Django 를 활용한 다양한 API

## Used To
- Framework : Django
- Databases : SQLite
- Caches : Redis
- Container : Docker

## Apps

> ### User
> - Oauth2 기반 사용자 관리
> - 클라이언트 키와 시크릿 키를 이용한 토큰 발급
> - 기능별 Permission 설정
> - 소셜 로그인 추가(구글)
> - 이메일 주소를 기반으로 로컬, 소셜 사용자 통합 관리

> ### Token
> - Access Token, Refresh Token 로 구분하여 발급
> - Token White List 를 이용해 신규 발급 Token 만 유효하도록 설정
> - Cache 에 White List 를 저장하여 빠른 검사

> ### Notification
> - Naver Cloud SENS 서비스를 이용한 SMS 발송
> - 구글 API를 이용한 Mail 발송 서비스
> - Slack 메신저 발송
> - Twilio API 를 이용해 SMS, Call 발송

> ### Celery
> - 비동기 테스크 관리
> - background_task 와 함께 사용

> ### Scheduler
> - 스케쥴링 서비스 추가(APScheduler 사용)
> - Sqlite 메모리를 이용하여 스케쥴 보존

> ### 카카오
> - 카카오 토큰 발급/재발급
> - 나에게 메시지 전송
> - 챗봇 메모 기능 추가
> - 카카오 AI 오픈 소스를 이용해 자동 답변 기능 추가
> - 스케쥴링 서비스와 연동하여 알람 기능 추가
> - 친구에게 메시지 보내기
> - 친구 목록 조회 등(준비중)

> ### Security
> - RSA 256 방식의 암호화
> - 공개키/비밀키를 이용

> ### ETC
> - 데이터베이스 데이터 암호화
> - docker-compose 를 통해 일괄 생성
> - Logger 추가(SQLite 에 저장 및 Middleware 에 등록)
> - FTP 에 이미지 등록


## Run

Git Clone :

```sh
git clone https://github.com/ja-y-com/django.git
```

환경 변수 생성 : `.env`, `.build 내 환경 설정 파일`

기본 명령어 :

```sh
python manage.py runserver
```

## Document

Django 에서 추가로 설치한 `Swagger`를 이용하였습니다.

_API에 관한 기본적인 정보는 물론 직접 `테스트`도 가능합니다._

서버 실행 후 http://localhost/swagger 에서 확인 가능합니다.

## Environment

프로그램 실행을 위해선 아래 버전 준수가 요구됩니다.

```sh
Python 3.8 이상
```

## Update

* 0.0.1
  * 최초 배포

## Contact

JAY | root@ja-y.com
