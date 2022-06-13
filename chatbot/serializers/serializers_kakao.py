import datetime

from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import empty

from core.consts import KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE
from core.keys import generate_random_number
from core.models import ProjectConstant
from core.serializers import DoesntStoreSerializer
from chatbot.models import ChatbotFriend, ChatbotContent, ChatbotContentText


class ChatbotCreateBotSerializer(DoesntStoreSerializer):
    id = serializers.CharField()
    name = serializers.CharField()


class ChatbotCreateIntentExtraReasonSerializer(DoesntStoreSerializer):
    code = serializers.IntegerField()
    message = serializers.CharField()


class ChatbotCreateIntentExtraSerializer(DoesntStoreSerializer):
    reason = ChatbotCreateIntentExtraReasonSerializer()


class ChatbotCreateIntentSerializer(DoesntStoreSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    extra = ChatbotCreateIntentExtraSerializer()


class ChatbotCreateActionParamsSerializer(DoesntStoreSerializer):
    user_id = serializers.CharField(required=False)


class ChatbotCreateActionDetailParamsSerializer(DoesntStoreSerializer):
    pass


class ChatbotCreateActionClientExtraSerializer(DoesntStoreSerializer):
    pass


class ChatbotCreateActionUserRequestBlockSerializer(DoesntStoreSerializer):
    id = serializers.CharField()
    name = serializers.CharField()


class ChatbotCreateActionUserRequestUserPropertiesSerializer(DoesntStoreSerializer):
    botUserKey = serializers.CharField()
    isFriend = serializers.BooleanField(
        default=False
    )
    plusfriendUserKey = serializers.CharField()
    bot_user_key = serializers.CharField()
    plusfriend_user_key = serializers.CharField()


class ChatbotCreateActionUserRequestUserSerializer(DoesntStoreSerializer):
    id = serializers.CharField()
    type = serializers.CharField()
    properties = ChatbotCreateActionUserRequestUserPropertiesSerializer()


class ChatbotCreateActionUserRequestParamsMediaSerializer(DoesntStoreSerializer):
    type = serializers.CharField()
    url = serializers.CharField()


class ChatbotCreateActionUserRequestParamsSerializer(DoesntStoreSerializer):
    surface = serializers.CharField()
    media = ChatbotCreateActionUserRequestParamsMediaSerializer(required=False)


class ChatbotCreateActionUserRequestSerializer(DoesntStoreSerializer):
    block = ChatbotCreateActionUserRequestBlockSerializer()
    user = ChatbotCreateActionUserRequestUserSerializer()
    utterance = serializers.CharField()
    params = ChatbotCreateActionUserRequestParamsSerializer()
    lang = serializers.CharField()
    timezone = serializers.CharField()


class ChatbotCreateActionSerializer(DoesntStoreSerializer):
    id = serializers.CharField()
    name = serializers.CharField()
    params = ChatbotCreateActionParamsSerializer()
    detailParams = ChatbotCreateActionDetailParamsSerializer()
    clientExtra = ChatbotCreateActionClientExtraSerializer()


class ChatbotCreateSerializer(DoesntStoreSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if data != empty:
            self.response_text = ProjectConstant.get_constant(
                "MEMO_DEFAULT_RESPONSE_TEXT"
            )
            self.response_quick_replies = []

    bot = ChatbotCreateBotSerializer()
    intent = ChatbotCreateIntentSerializer()
    action = ChatbotCreateActionSerializer()
    userRequest = ChatbotCreateActionUserRequestSerializer()
    contexts = serializers.ListSerializer(child=serializers.CharField())

    @property
    def response_template(self):
        """
        답변 템플릿
        :return:
        """
        template = KAKAO_CHAT_BOT_DEFAULT_SIMPLE_TEXT_MESSAGE
        template["template"]["quickReplies"] = self.response_quick_replies
        template["template"]["outputs"][0]["simpleText"][
            "text"
        ] = self.response_text
        return template

    def save(self, **kwargs):
        # 데이터 조회
        content = self.validated_data.get("userRequest", {}).get("utterance")
        user_key = (
            self.validated_data.get("userRequest", {})
            .get("user", {})
            .get("properties", {})
            .get("bot_user_key")
        )
        # 데이터 생성
        with transaction.atomic():
            friend_obj, _ = ChatbotFriend.objects.get_or_create(user_key=user_key)
            # ----------
            # 1. 일반 메모
            # ----------
            content_obj = ChatbotContentText.objects.create(content=content)
            ChatbotContent.objects.create(
                friend=friend_obj,
                content_object=content_obj
            )

    def to_representation(self, instance):
        return self.response_template


class ChatbotListSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        label="컨텐츠",
        source="content_object.content",
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = ChatbotContent
        fields = ("content",)
