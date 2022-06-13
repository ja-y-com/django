from django.db import models


class WeekChoices(models.IntegerChoices):
    MON = 0, "월"
    TUE = 1, "화"
    WED = 2, "수"
    THU = 3, "목"
    FRI = 4, "금"
    SAT = 5, "토"
    SUN = 6, "일"
