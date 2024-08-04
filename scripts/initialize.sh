# 프로젝트 디렉터리로 이동
cd /home/ubuntu/Zipbab-Coin-BE/Zipbab

# 가상환경 실행
source venv/bin/activate

# 가상환경 실행 후, 필요한 패키지 설치
pip install -r requirements.txt
pip install uwsgi
sudo apt-get install nginx