cd /home/ubuntu/Zipbab-Coin-BE/Zipbab

# 가상환경 실행
source venv/bin/activate

# uWSGI 마스터 프로세스의 PID 찾기
UWSGI_PID=$(pgrep -f "uwsgi --ini uwsgi.ini" | head -n 1)

if [ -z "$UWSGI_PID" ]; then
    echo "실행 중인 uWSGI 프로세스를 찾을 수 없습니다."
    exit 1
fi

echo "uWSGI 마스터 프로세스 PID: $UWSGI_PID"

# 프로세스 종료
echo "uWSGI 프로세스를 종료합니다..."
kill -TERM $UWSGI_PID

# 프로세스가 종료될 때까지 대기
wait $UWSGI_PID

echo "uWSGI 프로세스가 종료되었습니다."

# uwsgi 실행
uwsgi --ini uwsgi.ini

# nginx 재시작
sudo service nginx restart