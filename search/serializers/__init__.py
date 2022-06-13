from django.conf import settings
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from advance_payment.models import InstantPayUseHistory, AdvancePaymentProviderProfile
from advance_payment.serializers import PlatformFeeSerializer
from core.choices import BASE_EVENTS_TITLE
from core.serializers import DoesntStoreSerializer

from core.utils import TimeZoneUtil
from instantpay_promotion.models import PlatformFeeCoupon
from legacies.models import Member, Company
from mileages.models import MileageDashboard, ServiceMileage
from notifications.models import TargetUserPushNotification, NotificationTargetUser


allow_keys = ['name', 'age', 'gender', 'uses_count', 'companies']
# 개인별 (이름검색)
# 연령별
# 성별
# 선지급 사용 횟수별
allow_operators = ['&', '|', '!']


def validate_search_key(key):
    if key not in allow_keys:
        raise serializers.ValidationError()


def validate_search_operator(op):
    if op not in allow_operators:
        raise serializers.ValidationError()


class CharOrListField(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class SearchUnitSerializer(DoesntStoreSerializer):
    key = serializers.CharField(
        label='항목명', validators=[validate_search_key],
        help_text='이름: name, 나이: age (1980-1990), 성별: gender (M or W), '
                  '선지급 사용횟수: uses_count, 회사: companies (c_idx array)'
    )
    value = CharOrListField(label='항목별 값', help_text='일반적으로는 string, 기업일 경우 [Integer]')
    value_operator = serializers.CharField(
        label='연산자', validators=[validate_search_operator],
        help_text='&: AND, |: OR, !: NOT'
    )
    comparison_operator = serializers.CharField(
        label='비교 연산 (횟수 연산시 사용)', required=False,
        help_text='G: Greater than, L: Less than, E: Equals'
    )


class SearchUserResultsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(label='이름')
    email = serializers.SerializerMethodField(label='이메일')
    birth = serializers.SerializerMethodField(label='생년월일')
    phone = serializers.SerializerMethodField(label='휴대폰번호')
    company = serializers.SerializerMethodField(label='소속기업')
    gender = serializers.SerializerMethodField(label='성별')
    uses_number = serializers.SerializerMethodField(label='선지급 사용횟수 (당월)')
    total_uses_number = serializers.SerializerMethodField(label='선지급 사용횟수 (총 누적)')

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_name(self, obj):
        return obj.get_name

    @swagger_serializer_method(serializer_or_field=serializers.EmailField())
    def get_email(self, obj):
        return obj.profile.email

    @swagger_serializer_method(serializer_or_field=serializers.DateField())
    def get_birth(self, obj):
        return obj.profile.birth

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_phone(self, obj):
        return obj.profile.phone

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_company(self, obj):
        pair = obj.company_pair.filter(is_active_context=True).first()
        if pair:
            return pair.company.c_name
        return '소속 기업 없음'

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_gender(self, obj):
        return obj.m_gender

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_uses_number(self, obj):
        this_month = TimeZoneUtil.seoul_zone_now().date()
        return InstantPayUseHistory.objects.filter(
            provider_contract__pay_contract__user_pair__user=obj,
            created__month=this_month.month,
            created__year=this_month.year,
        ).count()

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField())
    def get_total_uses_number(self, obj):
        return InstantPayUseHistory.objects.filter(provider_contract__pay_contract__user_pair__user=obj).count()

    class Meta:
        model = Member
        fields = (
            'm_idx', 'name', 'email', 'birth', 'phone',
            'company', 'gender', 'uses_number', 'total_uses_number'
        )


class SearchCompanyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('c_idx', 'c_name')


class ServiceMileageSerializer(serializers.ModelSerializer):
    target_users = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True, allow_empty=False
    )

    giver_id = serializers.IntegerField(label='지급하는 사용자 m_idx', required=True)

    def save(self, **kwargs):
        target_users = self.validated_data.get('target_users')
        giver = self.validated_data.get('giver_id')
        memo = self.validated_data.get('memo')
        amount = self.validated_data.get('amount')
        for user in target_users:
            u = Member.objects.get(m_idx=user)
            dashboard_set = MileageDashboard.objects.filter(user=u)
            if dashboard_set.exists():
                dashboard = dashboard_set.first()
            else:
                dashboard = dashboard_set.create(user=u, )
            ServiceMileage.objects.create(
                dashboard=dashboard,
                giver=Member.objects.get(m_idx=giver),
                memo=memo,
                amount=amount,
            )

    class Meta:
        model = ServiceMileage
        fields = ('amount', 'memo', 'giver_id', 'target_users',)


class PushMessageSerializer(serializers.ModelSerializer):
    target_users = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True, allow_empty=False
    )

    def save(self, **kwargs):
        data = self.validated_data
        target_users = data.get('target_users')
        subject = data.get('subject')
        contents = data.get('contents')
        schedule_at = data.get('schedule_at')
        repeat = data.get('repeat')
        how_due = data.get('how_due')
        request = self.context.get('request')
        noti = TargetUserPushNotification.objects.create(
            sender=request.user,
            subject=subject,
            contents=contents,
            schedule_at=schedule_at,
            repeat=repeat,
            how_due=how_due,
        )

        for user in target_users:
            NotificationTargetUser.objects.create(
                user=Member.objects.get(m_idx=user),
                notification=noti
            )
            pass

        if not settings.TEST:
            from notifications.tasks import send_notification
            send_notification.delay(noti.id, 'TargetUserPushNotification')
        pass

    class Meta:
        model = TargetUserPushNotification
        fields = ('subject', 'contents', 'schedule_at', 'repeat', 'how_due', 'target_users',)

    pass


class SignInSerializer(DoesntStoreSerializer):
    username = serializers.CharField(label='사용자명', required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(label='비밀번호', required=True, allow_null=False, allow_blank=False)


class RefreshTokenSerializer(DoesntStoreSerializer):
    refresh_token = serializers.CharField(label='리프레시 토큰')

    def validate(self, attrs):
        from oauth2_provider.models import RefreshToken
        from rest_framework.generics import get_object_or_404
        self.refresh_token = get_object_or_404(RefreshToken, token=attrs.get('refresh_token'))
        return attrs


class FeeCouponSerializer(serializers.ModelSerializer):
    target_users = serializers.ListSerializer(
        child=serializers.IntegerField(), required=True, allow_empty=False
    )

    target_profile_id = serializers.IntegerField(label='', required=False)

    def save(self, **kwargs):

        target_users = self.validated_data.get('target_users')
        name = self.validated_data.get('name')
        target_profile_id = self.validated_data.get('target_profile_id')
        expire_on = self.validated_data.get('expire_on')
        coupon_type = self.validated_data.get('coupon_type')
        discount = self.validated_data.get('discount')

        if target_profile_id:
            target_profile = get_object_or_404(AdvancePaymentProviderProfile, id=target_profile_id)
        else:
            target_profile = None

        coupons = []

        for user in target_users:
            coupons.append(PlatformFeeCoupon(
                name=name,
                target_user=Member.objects.get(m_idx=user).company_pair.filter(is_active_context=True).first(),
                target_profile=target_profile,
                expire_on=expire_on,
                coupon_type=coupon_type,
                discount=discount,
            ))
            pass
        PlatformFeeCoupon.objects.bulk_create(coupons)

        pass

    class Meta:
        model = PlatformFeeCoupon
        fields = ('target_users', 'name', 'target_profile_id', 'expire_on', 'coupon_type', 'discount',)


class AdminProviderProfileListSerializer(serializers.ModelSerializer):
    provider_name = serializers.SerializerMethodField(label='서비스 제공사')
    platform_fee = PlatformFeeSerializer(label='수수료')

    @swagger_serializer_method(serializer_or_field=serializers.CharField())
    def get_provider_name(self, obj):
        return obj.provider.provider

    class Meta:
        model = AdvancePaymentProviderProfile
        fields = ('provider_name', 'name', 'is_default', 'platform_fee', 'ratio', 'delay_ratio', 'grace_period')
