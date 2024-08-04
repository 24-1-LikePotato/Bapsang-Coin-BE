cd /home/ubuntu/Zipbab-Coin-BE/Zipbab

# 가상환경 실행
source venv/bin/activate

git pull

# uwsgi 실행
uwsgi --ini uwsgi.ini

# nginx 재시작
sudo service nginx restart