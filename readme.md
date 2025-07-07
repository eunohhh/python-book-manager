# Python Book Manager

이 레포는 FastAPI, SQLite, Docker를 활용한 간단한 도서 관리 백엔드 예제입니다. 도서의 CRUD(생성, 조회, 수정, 삭제) 기능을 제공합니다.

## 실행 방법

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
uvicorn app.main:app --reload
```
