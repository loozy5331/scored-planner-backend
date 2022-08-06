# scored-planner-backend
점수 계획표 백엔드 서버

- main: fastAPI의 메인
- models: 데이터 클래스 모음
- middleware: 모든 API에서 동작하는 중간 계층
- exceptions: 정의된 예외들
- dependencies: 외부 의존성 코드(현재 JWT만 사용 중)
- db: DB 연결부
- router: API 라우터

> 라이브러리
> - fastapi: 기본 프레임워크
> - psycopg2-binary: postgreSQL과 연결하기 위한 RDBMS
> - python-jose: jwt 토큰 발급
> - uvicorn: 일종의 리버스 프록시 서버
> - pymongo: mongoDB를 활용
> - opensearch-py: AWS opensearch를 활용

## API 설계 구조
호출 형태 정의
| Method | API | Description |
| --- | --- | --- |

---
## 고려사항 및 설계 포인트
### 1. 라우터를 통한 서비스 로직 분리
### 2. 외부 모듈 분리
### 3. SQL 사용을 통한 확장성 확보

---
## 실행 방법
1. docker 설치
2. 도커 파일 빌드 및 실행
```sh
docker build -t backend .
docker run --rm -it -p 8000:8000 backend
```
* 호스트 서버의 8000번 포트로 API 호출 가능 ("http://localhost:8000")
    - FastAPI 기본 포트 8000 사용
    - Dockerfile 수정을 통해 변경 가능
* (optional) FastAPI에서 기본으로 제공하는 "http://localhost:8000/docs"를 통해 API 호출 가능

---
## TODO
1. API 경로 재설계 필요
경로가 너무 무분별함
2. 코드의 리펙토링이 필요
가능하다면 추가적인 분리가 필요(ex. 별도의 인증서버)