import os
import json
import uuid
import datetime
from typing import Any, Dict, List, Optional, Union
import logging

# 로거 설정
logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """
    UUID 생성
    
    Returns:
        UUID 문자열
    """
    return str(uuid.uuid4())

def to_camel(snake_str: str) -> str:
    """
    스네이크 케이스를 카멜 케이스로 변환
    
    Args:
        snake_str: 스네이크 케이스 문자열
        
    Returns:
        카멜 케이스 문자열
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])

def to_snake(camel_str: str) -> str:
    """
    카멜 케이스를 스네이크 케이스로 변환
    
    Args:
        camel_str: 카멜 케이스 문자열
        
    Returns:
        스네이크 케이스 문자열
    """
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

def json_serializer(obj: Any) -> str:
    """
    JSON 직렬화 함수
    
    Args:
        obj: 직렬화할 객체
        
    Returns:
        JSON 문자열
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def parse_json(json_str: str) -> Dict[str, Any]:
    """
    JSON 문자열 파싱
    
    Args:
        json_str: JSON 문자열
        
    Returns:
        파싱된 딕셔너리
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 파싱 오류: {e}")
        return {}

def get_env_var(name: str, default: Optional[str] = None) -> str:
    """
    환경 변수 조회
    
    Args:
        name: 환경 변수 이름
        default: 기본값
        
    Returns:
        환경 변수 값
    """
    return os.getenv(name, default)

def format_datetime(dt: datetime.datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    날짜 형식 변환
    
    Args:
        dt: 날짜 객체
        format_str: 형식 문자열
        
    Returns:
        형식화된 날짜 문자열
    """
    return dt.strftime(format_str)

def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime.datetime:
    """
    날짜 문자열 파싱
    
    Args:
        dt_str: 날짜 문자열
        format_str: 형식 문자열
        
    Returns:
        파싱된 날짜 객체
    """
    return datetime.datetime.strptime(dt_str, format_str)

def truncate_string(text: str, max_length: int = 100) -> str:
    """
    문자열 자르기
    
    Args:
        text: 원본 문자열
        max_length: 최대 길이
        
    Returns:
        잘린 문자열
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..." 