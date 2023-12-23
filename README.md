## 사용 언어, 프레임워크
- FastAPI, SQLAlchemy

## docker container로 실행하기
```
1. docker build -t myapp .
2. docker run -d -p 80:80 --env-file .env myapp
```
- myapp은 컨테이너 이름으로 대체

## 시작하기 전에
DB 테이블을 추가하기 위해서는 아래 커맨드를 입력하여 alembic script를 통해 추가해야 합니다
1. poetry 설치
```
pip install poetry
```
2. 패키지 설치
```
poetry lock
```
3. alembic script로 DB 테이블 추가
```
alembic upgrade head
```

## API 및 설계 관련
- 초성 검색을 위해서 Product 테이블에 데이터를 저장할 때 초성을 같이 저장하도록 구현하였습니다.
이에 따라 초성 검색을 하는 경우에는 해당 초성 테이블에 대한 Like 검색을 하도록 하였습니다.
