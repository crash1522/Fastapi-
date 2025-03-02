import uvicorn
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

if __name__ == "__main__":
    # 환경 변수에서 설정 가져오기
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    
    print(f"서버 시작: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"API 문서: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/docs")
    
    # 서버 실행
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    ) 