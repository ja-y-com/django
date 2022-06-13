from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from encrypted_fields.fields import EncryptedFieldMixin, SearchField


class PhoneNumberValidation:
    """
    휴대폰 번호 유효성 검사
    """

    def _length_validate(self, value):
        # 국내 휴대폰 번호 자리수 확인
        if not 9 < len(value) < 12:
            raise Exception("The length of the value must be 10, 11.")
        return value

    def _type_validate(self, value):
        # 숫자인지 확인
        if not str(value).isdecimal():
            raise Exception("Type Error")
        return value

    def phone_number_validate(self, value):
        if value is not None:
            # 불필요한 문자 제거
            value = str(value).replace("-", "").strip()
            value = self._length_validate(value)
            value = self._type_validate(value)
        return value


class PhoneNumberField(CharField, PhoneNumberValidation):
    """
    휴대폰 번호 기본 필드
    """

    description = _("Phone Number")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 15)
        super().__init__(*args, **kwargs)

    @classmethod
    def _set_phone_number_format(cls, value):
        if value is None:
            return value
        # 자리수별 포멧 적용
        if len(value) == 11:
            return f"{value[:3]}-{value[3:7]}-{value[7:]}"
        elif len(value) == 10:
            return f"{value[:3]}-{value[3:6]}-{value[6:]}"
        else:
            return value

    def get_prep_value(self, value):
        """
        데이터 저장 전 수정
        """
        value = self.phone_number_validate(value)
        value = self.to_python(value)
        return super().get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        """
        데이터 호출 시 수정
        """
        return self._set_phone_number_format(self.to_python(value)) if value else None


class PhoneNumberSearchField(SearchField, PhoneNumberValidation):
    """
    휴대폰 번호 검색 필드
    """

    def get_prep_value(self, value):
        """
        데이터 저장 전 수정
        """
        value = self.phone_number_validate(value)
        return super().get_prep_value(value)


class PhoneNumberEncryptedField(EncryptedFieldMixin, PhoneNumberField):
    """
    휴대폰 번호 암호화 필드
    """

    def from_db_value(self, value, expression, connection):
        """
        데이터 호출 시 수정
        """
        value = super().from_db_value(value, expression, connection)
        return self._set_phone_number_format(value)
