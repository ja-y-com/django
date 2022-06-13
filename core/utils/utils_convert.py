def second_to_simple(second: int) -> str:
    """
    초 단위를 간단한 텍스트로 전환
    ex. 60s > 1m
    """
    if 0 < second < 60:
        return f"{second}s"
    elif 60 < second < 3600:
        return f"{second//60}m"
    elif 3600 < second < 86400:
        return f"{second // 3600}h"
    return f"{second//86400}d"
