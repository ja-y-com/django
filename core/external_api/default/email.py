from django.conf import settings


def send_email(data: dict):
    """
    이메일 발송 - 단순 텍스트 발송
    """
    from django.core.mail import EmailMessage

    subject = data.get("subject")
    body = data.get("message")
    to = data.get("target")

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[to]
    )
    email.send()

    return email
