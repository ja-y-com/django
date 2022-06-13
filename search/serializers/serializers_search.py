from typing import List, Dict

from core.consts import (
    SEARCH_MEMBER_KEYWORDS, SEARCH_COMPANY_KEYWORDS
)
from core.serializers import DoesntStoreSerializer
from rest_framework import serializers

from legacies.models import Company, Member


class SearchSerializer(DoesntStoreSerializer):
    searchKey = serializers.CharField(
        label="항목명",
        help_text=(
            "통합 검색 항목 명<br>"
            "통합 검색 기획서 참고"
        ),
        write_only=True
    )
    searchValue = serializers.DictField(
        label="항목별 값",
        help_text=(
            "항목별로 값의 형태가 다를 수 있음<br>"
            "일반 텍스트는 textValue<br>"
            "범위의 경우 startValue, endValue 로 전달"
        ),
        write_only=True
    )


class SearchListSerializer(DoesntStoreSerializer):
    queries = serializers.ListSerializer(
        label="검색 리스트",
        child=SearchSerializer(),
        write_only=True,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset: dict = {}
        # 키워드 셋
        self.all_keywords_set = [
            (SEARCH_MEMBER_KEYWORDS, Member),
            (SEARCH_COMPANY_KEYWORDS, Company),
            # ---------------------------
            # 추가되는 키워드는 아래에 이어서 작성
            # ---------------------------
        ]
        # 전체 키워드
        self.all_keywords = sum(list(map(lambda x: x[0], self.all_keywords_set)), [])

    def keyword_to_model_and_name(self, keyword):
        """
        키워드에 맞는 모델과 클래스명 검색
        """
        for keywords, model in self.all_keywords_set:
            if keyword in keywords:
                return model.objects, model.__name__
        else:
            return None, None

    @property
    def key_set(self) -> dict:
        """
        키워드별로 모델 메니저 지정
        """
        return {
            keyword: self.keyword_to_model_and_name(keyword)
            for keyword in self.all_keywords
        }

    def set_models_queryset(self, queries: List[Dict]):
        """
        검색 쿼리별 쿼리셋 조회
        """
        # 데이터가 없는 경우 빠져나가기
        if queries is None or len(queries) == 0:
            return

        # 데이터 조회
        query = queries.pop()
        key, value = query.values()

        # 모델 메니저 조회
        model_manager, model_name = self.key_set[key]
        if model_name in self.queryset.keys():
            # 이미 조회한 쿼리가 있는 경우 그걸 활용
            model_manager = self.queryset.get(model_name)

        # 쿼리셋 조회
        queryset = model_manager.search(
            key=key,
            value=value,
        )

        # 조회된 데이터 저장
        self.queryset[model_name] = queryset
        # 다음 데이터 조회
        self.set_models_queryset(queries)

    def to_representation(self, instance) -> dict:
        """
        쿼리셋 조회 및 결과 반환
        """
        self.set_models_queryset(self.validated_data.get("queries"))
        results = {
            key: list(value.values_list(
                # 인덱스 값만 가져오기
                value.model._meta.pk.attname, flat=True
            ))
            for key, value in self.queryset.items()
        }
        return {"results": results}
