

# 사용 기술
- Django
- Gunicorn
- DRF
- Docker
- PostgreSQL


## 0. pipx 설치 

[참고 문서](https://pipx.pypa.io/stable/installation/)
### Ubuntu
```shell
sudo apt update
sudo apt install pipx
pipx ensurepath

vim ~/.bashrc
```

- bashrc 최하단에 사진과 같이 기입 후 저장

![image](https://github.com/user-attachments/assets/d9e08953-87ba-4876-9036-5a375b1cd994)

```text
export PATH="$HOME/.local/bin:$PATH"
```

- bashrc 변경사항 적용
```shell
source ~/.bashrc
```

### MacOS
```shell
brew install pipx
pipx ensurepath
sudo pipx ensurepath --global
```

## 1. poetry 설치
[참고문서](https://python-poetry.org/docs/#installation)
### Ubuntu
```shell
pipx install poetry
```

## 2. 프로젝트 클론 및 의존성 설치
```shell
git clone -b main https://github.com/chaechaeis/capstoneBE.git
cd path/to/project
poetry config virtualenvs.in-project true
poetry install --no-root
```

## 3. 가상환경 실행
```shell
poetry shell
```

## 4. Database migration
```shell
python manage.py migrate
```

## 5. 서버 실행
```shell
python manage.py runserver
```

## Production

> 추후 배포 과정은 자동화 예정입니다.

### 도커 이미지 생성 및 PUSH/PULL
```shell
docker build . -t <dockerhub_name>/upcy-be:latest
docker push <dockerhub_name>/upcy-be:latest
```

> EC2에 접속하여 도커허브에 PUSH한 이미지를 내려받습니다.
```shell
docker pull <dockerhub_name>/upcy-be:latest
```

### 컨테이너 실행 방법
```shell
sudo docker run -d --name upcy-be-container -p 8000:8000 <dockerhub_name>/upcy-be:latest # EC2에서 실행
sudo docker container ls # 실행중인 컨테이너 리스트 확인
sudo docker logs -f {container_id} # 콘솔 로그 보는 방법
```
