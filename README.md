# Weaviate & Python 프로젝트 설정

이 프로젝트는 Docker Compose를 사용하여 `Weaviate`를 실행하고, Python 환경에서 `weaviate-client`를 사용하여 데이터를 처리하는 프로젝트입니다. 아래의 단계를 따라 프로젝트를 설정하고 실행할 수 있습니다.

## 요구 사항

- Docker
- Docker Compose
- Python 3.x
- pip3

## 설정 방법

### 1. **Docker Compose로 Weaviate 실행**

Weaviate는 `docker-compose.yml` 파일을 사용하여 Docker에서 실행됩니다.

#### 1.1. Weaviate 컨테이너 실행

```bash
# Docker Compose로 Weaviate 컨테이너를 백그라운드에서 실행합니다.
docker-compose up -d
```

Weaviate가 실행되면, 로컬 머신에서 `http://localhost:8080`을 통해 Weaviate API에 접근할 수 있습니다.

### 2. **Python 환경 설정**

#### 2.1. Python 의존성 설치

`requirements.txt` 파일을 사용하여 필요한 Python 패키지를 설치합니다.

```bash
# 필요한 Python 패키지를 설치합니다.
pip3 install -r requirements.txt
```

#### 2.2. `install_dependencies.sh` 스크립트 실행 (선택 사항)

아래 스크립트를 사용하여 의존성 패키지를 설치할 수 있습니다.

```bash
# install_dependencies.sh 스크립트를 실행하여 의존성 패키지를 설치합니다.
bash install_dependencies.sh
```

### 3. **Weaviate API와 연결**

Weaviate와 연결하는 Python 코드 예시입니다. 이 코드는 `weaviate-client` 라이브러리를 사용하여 데이터를 가져오는 예시입니다.

```python
import weaviate

# Weaviate에 연결
client = weaviate.Client("http://localhost:8080")

# Weaviate에서 데이터 가져오기 예시
result = client.query.get("YourClass", ["property1", "property2"]).do()
print(result)
```

이 코드를 실행하여 Weaviate에 쿼리를 보내고 데이터를 가져올 수 있습니다.

### 4. **서버 실행 (Flask API 예시)**

서버를 Flask로 실행하려면, 아래와 같은 코드로 API 서버를 실행할 수 있습니다. 예를 들어:

```python
from flask import Flask, jsonify
import weaviate

app = Flask(__name__)

# Weaviate 연결
client = weaviate.Client("http://localhost:8080")

@app.route('/query')
def query():
    # Weaviate에서 데이터 가져오기 예시
    result = client.query.get("YourClass", ["property1", "property2"]).do()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
```

이 코드로 Flask 서버를 실행하면, `http://localhost:5050/query`에서 Weaviate 데이터를 반환하는 API를 사용할 수 있습니다.

```bash
curl --location --request GET 'http://localhost:5050/query' \
--header 'Content-Type: application/json' \
--data '{"query": "SK텔레콤의 최고경영자(CEO)는 누구인가요?"}'
```

### 5. **컨테이너 중지**

Weaviate 컨테이너를 중지하려면 아래 명령어를 사용합니다.

```bash
# Docker Compose로 실행된 Weaviate 컨테이너를 중지합니다.
docker-compose down
```

## Troubleshooting

- **Docker 포트 충돌**: 만약 `8080` 포트가 이미 다른 서비스에서 사용 중이라면, `docker-compose.yml` 파일에서 `8080:8080`을 다른 포트로 변경하여 실행할 수 있습니다.

- **403 에러**: Weaviate API에서 403 에러가 발생하는 경우, Weaviate의 인증 설정을 확인하거나 API 키를 설정해야 할 수 있습니다.
